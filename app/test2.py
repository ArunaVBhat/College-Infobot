import unittest
from unittest.mock import patch, mock_open
from infobot.routes import generate_response, admin_force_refresh
from infobot.routes import load_context_cache, save_context_cache
from flask import Flask


class TestInfoBot(unittest.TestCase):

    # Test generate_response when no relevant information is in the cache
    @patch("builtins.open", new_callable=mock_open, read_data="Some irrelevant cached content.")
    @patch("os.path.exists", return_value=True)
    def test_generate_response_no_relevant_info(self, mock_exists, mock_open_file):
        user_query = "vision of vdit?"
        response = generate_response(user_query)
        self.assertEqual(response["response"], "The provided website content does not mention the vision of Vdit.")
        self.assertEqual(response["source"], "No relevant chunks")

    # Test admin_force_refresh with Flask application context
    @patch("os.remove")
    @patch("infobot.routes.scrape_and_structure_website_selenium")
    @patch("os.path.exists", return_value=True)
    def test_admin_force_refresh(self, mock_exists, mock_scrape, mock_remove):
        app = Flask(__name__)
        with app.app_context():
            with patch("threading.Thread.start") as mock_thread:
                response = admin_force_refresh()

        self.assertEqual(response[1], 202)
        self.assertEqual(response[0].json["message"], "Background refresh started.")
        mock_remove.assert_called_once()
        mock_thread.assert_called_once()

    # Test generate_response when the cache is empty
    @patch("builtins.open", new_callable=mock_open, read_data="")
    @patch("os.path.exists", return_value=True)
    def test_generate_response_empty_cache(self, mock_exists, mock_open_file):
        user_query = "vision of vdit?"
        response = generate_response(user_query)
        self.assertEqual(response["response"], "No website context available.")
        self.assertEqual(response["source"], "No cache")

    # Test saving context cache
    @patch("builtins.open", new_callable=mock_open)
    def test_save_context_cache(self, mock_open_file):
        text_to_save = "This is some test context."
        save_context_cache(text_to_save)
        mock_open_file.assert_called_once_with("D:\\infobot4\\app\\infobot\\data\\context_cache.txt", "w",
                                               encoding="utf-8")
        mock_open_file().write.assert_called_once_with(text_to_save)

    # Test loading context cache
    @patch("builtins.open", new_callable=mock_open, read_data="This is some cached context.")
    @patch("os.path.exists", return_value=True)
    def test_load_context_cache(self, mock_exists, mock_open_file):
        context = load_context_cache()
        self.assertEqual(context, "This is some cached context.")
        mock_open_file.assert_called_once_with("D:\\infobot4\\app\\infobot\\data\\context_cache.txt", "r",
                                               encoding="utf-8")


if __name__ == "__main__":
    unittest.main()