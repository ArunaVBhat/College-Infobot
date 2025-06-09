from app import create_app  # Import the function that initializes Flask

app = create_app()  # Ensure app is created properly

if __name__ == "__main__":
    app.run()  # For local testing only
