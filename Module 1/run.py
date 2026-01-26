# Necessary modules to operate programs
from flask import Flask
import pages

def create_app():
    app = Flask(__name__)  # Create Flask object
    app.register_blueprint(pages.bp)  # Attach blueprint to main instance

    return app

# Run application
if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=8080, debug=True)