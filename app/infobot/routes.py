import logging
import os
import re
import threading
import time
import hashlib
from urllib.parse import urljoin
from flask import request, jsonify
from fuzzywuzzy import fuzz
import cohere
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from . import infobot_bp

# Logging config
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Initialize Cohere Client
co = cohere.Client(COHERE_API_KEY)

BASE_URL = "https://klsvdit.edu.in/"
context_chunks = []
context_text = ""

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTEXT_CACHE_PATH = os.path.join(BASE_DIR, "data", "context_cache.txt")

# In-memory query-response cache
query_cache = {}


def log_time_taken(step_name, start_time):
    """Log the time taken for a specific step."""
    end_time = time.time()
    duration = end_time - start_time
    logging.info(f"Step: {step_name} took {duration:.2f} seconds.")


def get_valid_sub_urls(soup, base_url, visited_urls):
    """
    Extract valid sub-URLs from the given BeautifulSoup object.
    """
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if (
                href.startswith("#") or
                'javascript:' in href.lower() or
                any(x in href.lower() for x in [
                    'facebook', 'instagram', 'linkedin', 'login', 'logout', 'mailto:', 'tel:'
                ])
        ):
            continue
        full_url = urljoin(base_url, href)
        if full_url not in visited_urls and full_url.startswith(base_url):
            links.append(full_url)
    return list(dict.fromkeys(links))


def load_context_cache():
    """Load cached context text from file, if present."""
    start_time = time.time()  # Start timing
    if os.path.exists(CONTEXT_CACHE_PATH):
        try:
            with open(CONTEXT_CACHE_PATH, "r", encoding="utf-8") as f:
                cached = f.read()
                if cached.strip():
                    logging.info(
                        f"Loaded cached context ({len(cached)} chars) from file (CACHE HIT). [Cache Path: {CONTEXT_CACHE_PATH}]")
                    log_time_taken("Load Context Cache", start_time)
                    return cached
                else:
                    logging.warning(
                        f"Context cache file exists but is empty (CACHE MISS). [Cache Path: {CONTEXT_CACHE_PATH}]")
        except Exception as e:
            logging.warning(f"Failed to read context cache: {e} [Cache Path: {CONTEXT_CACHE_PATH}]")
    else:
        logging.info(f"No context cache file found (CACHE MISS). [Cache Path: {CONTEXT_CACHE_PATH}]")
    log_time_taken("Load Context Cache", start_time)
    return None


def save_context_cache(text):
    """Save scraped context text to cache file."""
    start_time = time.time()  # Start timing
    try:
        with open(CONTEXT_CACHE_PATH, "w", encoding="utf-8") as f:
            f.write(text)
        logging.info(f"Saved scraped context to cache file at {CONTEXT_CACHE_PATH}.")
    except Exception as e:
        logging.warning(f"Failed to write context cache: {e} [Cache Path: {CONTEXT_CACHE_PATH}]")
    log_time_taken("Save Context Cache", start_time)


def split_context_to_chunks(context_text):
    """
    Split the context text into smaller chunks for better searchability.
    """
    start_time = time.time()
    chunks = []
    for block in context_text.split("\n\n"):
        block = block.strip()
        if len(block) > 40:
            chunks.append(block)
    log_time_taken("Split Context to Chunks", start_time)
    return chunks


def find_best_chunks(context_chunks, question, top_n=3):
    """
    Use fuzzy match to find the best matching chunks.
    """
    start_time = time.time()
    scores = [
        (chunk, fuzz.token_set_ratio(question.lower(), chunk.lower()))
        for chunk in context_chunks
    ]
    scores.sort(key=lambda x: -x[1])
    log_time_taken("Find Best Chunks", start_time)
    return [chunk for chunk, score in scores[:top_n] if score > 40]


def get_cached_response(query):
    """Retrieve cached response based on query hash."""
    query_hash = hashlib.sha256(query.encode()).hexdigest()
    return query_cache.get(query_hash)


def cache_response(query, response):
    """Cache the response for the given query."""
    query_hash = hashlib.sha256(query.encode()).hexdigest()
    query_cache[query_hash] = response
    logging.info(f"Cached response for query: {query}")


def generate_response(question):
    global context_text, context_chunks
    overall_start_time = time.time()

    # Check if response is already cached
    cache_check_start = time.time()
    cached_response = get_cached_response(question)
    log_time_taken("Check Cached Response", cache_check_start)
    if cached_response:
        logging.info("Cached response found.")
        log_time_taken("Overall Response Generation (Cached)", overall_start_time)
        return cached_response

    # Check context availability
    context_check_start = time.time()
    if not context_chunks:
        logging.warning("No context available from website scrape.")
        log_time_taken("Check Context Availability", context_check_start)
        return {
            "response": "I could not find the requested information on the official KLS VDIT website.",
            "source": "No website context available"
        }
    log_time_taken("Check Context Availability", context_check_start)

    # Find relevant chunks
    chunk_find_start = time.time()
    relevant_chunks = find_best_chunks(context_chunks, question)
    if not relevant_chunks:
        logging.info("No relevant context chunk found for query.")
        log_time_taken("Find Relevant Chunks", chunk_find_start)
        return {
            "response": "I could not find the requested information on the official KLS VDIT website.",
            "source": "No relevant context found"
        }
    log_time_taken("Find Relevant Chunks", chunk_find_start)

    context_for_prompt = "\n\n".join(relevant_chunks)

    # Generate response using Cohere API
    cohere_start = time.time()
    try:
        response = co.chat(
            model="command-xlarge-nightly",
            message=f"Answer ONLY using the following website content. "
                    f"If the answer is not present, say so clearly and do not make up information.\n\n"
                    f"Website Content:\n{context_for_prompt}\n\n"
                    f"User Question: {question}\n\n"
                    f"Answer:",
            max_tokens=4000,
            temperature=0.2,
        )
        reply = response.text.strip()
        last_fullstop = reply.rfind('.')
        if last_fullstop > 50:
            reply = reply[:last_fullstop + 1]
        log_time_taken("Cohere API Call", cohere_start)
        log_time_taken("Overall Response Generation", overall_start_time)

        if not reply:
            return {
                "response": "I could not find the requested information on the official KLS VDIT website.",
                "source": "No useful result from Cohere"
            }

        # Cache the generated response
        cache_response(question, {"response": reply, "source": "From website content"})
        return {"response": reply, "source": "From website content"}
    except Exception as e:
        logging.error(f"Cohere API error: {e}")
        log_time_taken("Cohere API Call", cohere_start)
        log_time_taken("Overall Response Generation", overall_start_time)
        return {
            "response": "Error occurred while processing your query.",
            "source": "Cohere API error"
        }


@infobot_bp.route("/query", methods=["POST"])
def query_handler():
    global context_chunks
    try:
        data = request.get_json()
        user_query = data.get("query", "").strip()

        start_time = time.time()
        logging.info(f"Received query: {user_query}")

        if not user_query:
            log_time_taken("Query Validation", start_time)
            return jsonify({"error": "Missing query"}), 400

        result = generate_response(user_query)
        log_time_taken("Query Handler", start_time)
        return jsonify(result), 200

    except Exception as e:
        logging.error(f"Query Handler Error: {e}")
        return jsonify({"error": str(e)}), 500


def scrape_and_structure_website_selenium(base_url, force_refresh=False):
    """
    Recursively scrape all sub-URLs of the base URL.
    - Starts from the base URL and follows all valid internal links.
    - Caches the scraped content to avoid redundant scraping.
    """
    global context_text, context_chunks

    if not force_refresh:
        cached = load_context_cache()
        if cached:
            context_text = cached
            context_chunks = split_context_to_chunks(context_text)
            logging.info(f"Context loaded from local cache file at: {CONTEXT_CACHE_PATH}")
            return

    context_pieces = []
    visited_urls = set()
    urls_to_scrape = [base_url]

    # Selenium options
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    logging.info("Starting Selenium WebDriver for scraping...")
    driver = webdriver.Chrome(options=chrome_options)

    def fetch_html(url):
        try:
            logging.info(f"Fetching URL with Selenium: {url}")
            driver.get(url)

            # Wait for the main content to load, with additional wait for dynamic elements
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )
            driver.implicitly_wait(5)  # Optional delay for slower pages

            html = driver.page_source
            return html
        except Exception as e:
            logging.warning(f"Failed to fetch {url} with Selenium: {e}")
            return ""

    def clean_soup_text(soup):
        """
        Extract all visible text while removing unnecessary tags.
        """
        for tag in soup(['script', 'style', 'form', 'input']):
            tag.decompose()
        texts = list(soup.stripped_strings)
        return "\n".join(texts)

    try:
        while urls_to_scrape:
            current_url = urls_to_scrape.pop(0)
            if current_url in visited_urls:
                continue
            logging.info(f"Scraping URL: {current_url}")
            html = fetch_html(current_url)
            visited_urls.add(current_url)
            if html:
                soup = BeautifulSoup(html, "html.parser")
                main_text = clean_soup_text(soup)
                if main_text.strip():
                    context_pieces.append(main_text)

                # Discover nested sub-URLs
                sub_urls = get_valid_sub_urls(soup, base_url, visited_urls)
                urls_to_scrape.extend(sub_urls)

    finally:
        driver.quit()

    context_text = "\n".join(context_pieces)
    context_chunks = split_context_to_chunks(context_text)
    if context_text.strip():
        save_context_cache(context_text)
        logging.info(f"Context scraped and saved to local cache file at: {CONTEXT_CACHE_PATH}")
    else:
        logging.error("Scraping finished but no content was found!")


@infobot_bp.route("/admin/refresh", methods=["POST"])
def admin_force_refresh():
    def background_scrape():
        try:
            scrape_start_time = time.time()
            scrape_and_structure_website_selenium(BASE_URL, force_refresh=True)
            log_time_taken("Background Scrape", scrape_start_time)
        except Exception:
            logging.exception("Scraping error")

    try:
        cache_removal_start = time.time()
        if os.path.exists(CONTEXT_CACHE_PATH):
            os.remove(CONTEXT_CACHE_PATH)
            logging.info("Old context cache removed.")
        log_time_taken("Cache Removal", cache_removal_start)

        threading.Thread(target=background_scrape).start()
        return jsonify({"message": "Background refresh started."}), 202
    except Exception:
        logging.exception("Refresh error")
        return jsonify({"error": "Refresh failed."}), 500