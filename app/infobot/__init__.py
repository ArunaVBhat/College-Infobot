from flask import Blueprint

infobot_bp = Blueprint("infobot", __name__)

from . import routes
from .routes import admin_force_refresh
from .routes import generate_response, load_context_cache, save_context_cache, scrape_and_structure_website_selenium