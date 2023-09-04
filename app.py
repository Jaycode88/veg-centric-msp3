# Import statements
import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Check for existence of 'env.py' and import if it exists
if os.path.exists("env.py"):
    import env

# Create a Flask application instance
app = Flask(__name__)

# Configure MongoDB settings using environment variables
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

# Set the secret key for Flask application
app.secret_key = os.environ.get("SECRET_KEY")

# tests 
print("MONGO_DBNAME:", app.config["MONGO_DBNAME"])
print("MONGO_URI:", app.config["MONGO_URI"])


try:
    db = PyMongo(app)
except Exception as e:
    print("Error initializing PyMongo:", e)


# Create a PyMongo instance linked to the Flask app for database access
# database = PyMongo(app)


# App routes
# Home page Recipes
@app.route("/")
@app.route("/show_recipes")
def show_recipes():
    recipes = list(db.db.recipes.find())
    return render_template("recipes.html", recipes=recipes)


# Run the Flask app if this script is the main entry point
if __name__ == "__main__":
    # Retrieve IP and PORT from environment variables
    host = os.environ.get("IP")
    port = int(os.environ.get("PORT"))

    # Run the app with debugging enabled (set to False upon project submission)
    app.run(host=host, port=port, debug=True)
