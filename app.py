# Import statements
import os
from flask import Flask

# Check for existence of 'env.py' and import if it exists
if os.path.exists("env.py"):
    import env

# Create a Flask application instance
app = Flask(__name__)


# Define a route for the root URL
@app.route("/")
def test():
    return "Flask app setup test"


# Run the Flask app if this script is the main entry point
if __name__ == "__main__":
    # Retrieve IP and PORT from environment variables
    host = os.environ.get("IP")
    port = int(os.environ.get("PORT"))

    # Run the app with debugging enabled (set to False upon project submission)
    app.run(host=host, port=port, debug=True)
