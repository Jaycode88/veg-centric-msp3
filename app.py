# Import statements
import os
import datetime
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

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

# Create a PyMongo instance linked to the Flask app for database access
database = PyMongo(app)


# App routes
# Home page Recipes
@app.route("/")
@app.route("/show_recipes")
def show_recipes():
    recipes = database.db.recipes.find()
    return render_template("recipes.html", recipes=recipes)


# sign up page
@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        # check passwords match
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        # if passwords dont match return flash message
        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(url_for("sign_up"))
        # Check username is not already taken
        existing_user = database.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            flash("Username already in use")
            return redirect(url_for("sign_up"))

        hashed_password = generate_password_hash(
            request.form.get("password"), method='pbkdf2:sha256',
            salt_length=16)
        register = {
            "firstname": request.form.get("firstname").lower(),
            "lastname": request.form.get("lastname").lower(),
            "email": request.form.get("email"),
            "username": request.form.get("username").lower(),
            "password": hashed_password,
            "member_since": datetime.datetime.now()
        }

        database.db.users.insert_one(register)

        # put new user into session(change this when sign in page is built,
        # request sign in after sign up complete)
        session["user"] = request.form.get("username").lower()
        flash("Sign Up Successful!")
        # change to url for profile when profile page is built
        return redirect(url_for("show_recipes", username=session["user"]))

    return render_template("sign_up.html")


# Run the Flask app if this script is the main entry point
if __name__ == "__main__":
    # Retrieve IP and PORT from environment variables
    host = os.environ.get("IP")
    port = int(os.environ.get("PORT"))

    # Run the app with debugging enabled (set to False upon project submission)
    app.run(host=host, port=port, debug=True)
