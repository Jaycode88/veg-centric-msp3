# Import modules
import os
import datetime
import cloudinary
from cloudinary.uploader import upload
import cloudinary.api
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

# configure Cloudinary settings using environment variables
cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET")
)

# Set the secret key for Flask application
app.secret_key = os.environ.get("SECRET_KEY")

# Create a PyMongo instance linked to the Flask app for database access
database = PyMongo(app)


# App routes

# Home page displaying Recipes for users in session
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


# homepage for users not in session
@app.route("/welcome")
def welcome():
    """
    Renders the welcome page.

    This route is used to display a welcome page for users who are not
    currently in a session. It provides information about the
    application and encourages users to sign in or create an account.

    Returns:
        flask.Response: The HTML response containing the welcome page.
    """
    return render_template("welcome.html")


# About page
@app.route("/about")
def about():
    """
    This function renders and displays the 'About' page.

    Returns:
        rendered HTML template for the About page.
    """
    return render_template("about.html")


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


# profile page
@app.route("/profile", methods=["GET", "POST"])
def profile():
    """
    Display the user's profile page if they are authenticated.

    Retrieves the username from the session, fetches user's data from database.
    If the user is in session, profile information is rendered on profile page.
    If the user is not in session, a flash message is displayed and
    they are redirected to the sign-in page.

    Returns:
        flask.Response: Renders profile page or redirects to the sign-in page.
    """
    username = session.get("user")

    if username:
        user = database.db.users.find_one({"username": username})
        user_recipes = database.db.recipes.find({"created_by": username})
        return render_template(
            "profile.html", user=user, user_recipes=user_recipes)
    else:
        # Handle case when the user is not in session
        flash("Please sign in to access your profile.")
        return redirect(url_for("sign_in"))


# Edit profile page
@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    # Get the current user's information from the database
    username = session.get("user")
    user = database.db.users.find_one({"username": username})

    if request.method == "POST":
        # Retrieve and update the user's information from the form
        user["firstname"] = request.form.get("firstname").capitalize()
        user["lastname"] = request.form.get("lastname").capitalize()
        user["email"] = request.form.get("email")

        # Retrieve the new password and confirm it
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        # Check if the new password matches the confirmation
        if new_password == confirm_password:
            # Hash the new password
            hashed_password = generate_password_hash(
                new_password, method='pbkdf2:sha256', salt_length=16)
            
            # Update the user's information in the database using update_one
            database.db.users.update_one({"_id": user["_id"]}, {"$set": {
                "firstname": user["firstname"],
                "lastname": user["lastname"],
                "email": user["email"],
                "password": hashed_password  # Update the password
            }})

            # Redirect to the user's profile page after editing
            return redirect(url_for("profile"))
        else:
            flash("Passwords do not match. Please try again.", "error")

    # Render the edit profile form
    return render_template("edit_profile.html", user=user)


# Delete profile page
@app.route("/delete_profile", methods=["GET", "POST"])
def delete_profile():
    # Get the current user's information from the session
    username = session.get("user")

    if username:
        # Fetch the user's data from the database
        user = database.db.users.find_one({"username": username})

    if request.method == "POST":
        # Delete the user's profile from the database
        database.db.users.delete_one({"username": username})

        # Clear the session to log the user out after deletion
        session.clear()

        # Redirect to a page after profile deletion (e.g., a thank you page)
        flash("Your profile has been deleted.")
        return redirect(url_for("welcome"))

    # Render the delete profile confirmation form
    return render_template("delete_profile.html", user=user)


# Add recipe page
@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    """
    Add a new recipe to the database.

    If method is POST, function extracts recipe information from the
    submitted form, validates it, adds recipe to db and
    uploads the recipe image to Cloudinary. If the method
    is GET, it renders the page to input a new recipe.

    Parameters:
    None

    Returns:
    GET Request:
        Render 'add_recipe.html' template inc. list categories for selection.

    POST Request:
        - If successful, flash message, redirect to 'show_recipes' page.
        - Validation errors, render 'add_recipe.html' with error messages.

    Dependencies:
    - The 'request' object from Flask to access form data.
    - The 'session' object to access the current user's information.
    - The 'datetime' module to record the date of recipe addition.
    - The 'database' object to interact with the database.
    - The 'upload' function to upload the recipe image to Cloudinary.

    Note:
    - Function assumes  existence of 'database.db.recipes', for recipe storage.
    - It expects fields named 'recipe_name', 'category', 'recipe_description',
      'method_step[]', 'ingredient[]', and 'quantity[]', 'recipe_image'.
      - The 'recipe_image' field should contain recipe's image file for upload.

    """
    if request.method == "POST":
        recipe_name = request.form.get("recipe_name")
        category = request.form.get("category")
        recipe_description = request.form.get("recipe_description")
        created_by = session["user"]
        ingredients = []
        method_step = request.form.getlist("method_step[]")
        date_added = datetime.datetime.now()
        formatted_date = date_added.strftime('%Y-%m-%d')

        # Upload the image to Cloudinary
        image_file = request.files["recipe_image"]
        if image_file:
            upload_result = upload(image_file)
            image_url = upload_result["secure_url"]

        for i in range(len(request.form.getlist("ingredient[]"))):
            ingredient = {
                "name": request.form.getlist("ingredient[]")[i],
                "quantity": request.form.getlist("quantity[]")[i]
            }
            ingredients.append(ingredient)

        recipe = {
            "recipe_name": recipe_name,
            "category": category,
            "recipe_description": recipe_description,
            "image": image_url,
            "created_by": created_by,
            "date_added": formatted_date,
            "ingredients": ingredients,
            "method_step": method_step
            }

        database.db.recipes.insert_one(recipe)
        flash("Recipe Successfully Posted")
        return redirect(url_for("show_recipes"))

    categories = database.db.categories.find().sort("category", 1)
    return render_template("add_recipe.html", categories=categories)


# view recipe page
@app.route("/recipe/<recipe_id>")
def view_recipe(recipe_id):
    """
    Display the details of a recipe.

    Parameters:
    - recipe_id (str): The unique identifier for the recipe.

    Returns:
    - str: HTML content for displaying the recipe details.

    Function fetches recipe details from database using the `recipe_id`,
    renders HTML template displaying those details,
    and returns the rendered HTML content.

    """
    # Fetch the recipe details from the database using the recipe_id
    recipe = database.db.recipes.find_one({"_id": ObjectId(recipe_id)})

    # Render the recipe details template and pass the recipe data
    return render_template("recipe_details.html", recipe=recipe)


# sign out function
@app.route("/sign_out")
def sign_out():
    """
    Sign out the user and redirect to the sign-in page.

    Displays a flash message to indicate successful logout,
    Removes the user from the session.

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
