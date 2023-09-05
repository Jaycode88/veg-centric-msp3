# Import modules
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

# Home page displaying Recipes
@app.route("/")
@app.route("/show_recipes")
def show_recipes():
    """
    Displays a list of recipes on the home page.

    Returns:
        Flask.render_template: HTML template rendering the list of recipes.
    """
    recipes = database.db.recipes.find()
    return render_template("recipes.html", recipes=recipes)


# sign up page
@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    """
    Handles user registration.

    Returns:
        Flask.redirect: Redirects to the sign-in page after sign up complete.
        Flask.render_template: HTML template rendering the sign-up page.
    """
    if request.method == "POST":
        # check passwords match
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        # if passwords dont match return flash error message
        if password != confirm_password:
            flash("Passwords do not match", "error")
            return redirect(url_for("sign_up"))
        # Check username is not already taken
        existing_user = database.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            flash("Username already in use")
            return redirect(url_for("sign_up"))
        # Hash the password using werkzueg and create user document
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

        # Insert user document to database
        database.db.users.insert_one(register)

        # Display a flash message indicating successful sign-up,
        # request sign_in
        flash("Sign Up Successful! Please now Sign in with your credentials")
        return redirect(url_for("sign_in"))

    # Render the sign up page
    return render_template("sign_up.html")


# sign in authenticate functions
def authenticate_user(username, password):
    """
    Authenticates a user based on their username and password.

    Args:
        username (str): The username provided by the user.
        password (str): The password provided by the user.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    # Check if the username exists in the database
    current_user = database.db.users.find_one({"username": username.lower()})

    if current_user:
        # Ensure hashed password matches user input
        if check_password_hash(current_user["password"], password):
            # put user into session
            session["user"] = username.lower()
            # Display welcome Flash message
            flash("Welcome, {}".format(username))
            return True
    return False


# sign in page
@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    """
    Handles user sign-in.

    Returns:
        Flask.redirect: Redirects to the profile page after successful sign-in.
        Flask.redirect: Redirect to sign-in with error flash if sign-in fails.
        Flask.render_template: HTML template rendering the sign-in page.
    """
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if authenticate_user(username, password):
            # redirect to show_recipes
            # change to url for profile when profile page built
            return redirect(url_for("show_recipes", username=session["user"]))
        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("sign_in"))

    # Render sign in page
    return render_template("sign_in.html")


# sign out function
@app.route("/sign_out")
def sign_out():
    """
    Sign out the user and redirect to the sign-in page.

    Displays a flash message to indicate successful logout and removes the user from the session.

    Returns:
        flask.Response: Redirects the user to the sign-in page.
    """
    flash("You have logged out")
    session.pop("user", None)
    return redirect(url_for("sign_in"))


# Run the Flask app if this script is the main entry point
if __name__ == "__main__":
    # Retrieve IP and PORT from environment variables
    host = os.environ.get("IP")
    port = int(os.environ.get("PORT"))

    # Run the app with debugging enabled (set to False upon project submission)
    app.run(host=host, port=port, debug=True)
