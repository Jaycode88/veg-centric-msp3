# Import modules
import os
import io
import datetime
import cloudinary
from PIL import Image
from cloudinary.uploader import upload
import cloudinary.api
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from settings import (
    MONGO_DBNAME, MONGO_URI, SECRET_KEY,
    CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET)

# Create a Flask application instance
app = Flask(__name__)

# Configure MongoDB settings using environment variables
app.config["MONGO_DBNAME"] = MONGO_DBNAME
app.config["MONGO_URI"] = MONGO_URI

# configure Cloudinary settings using environment variables
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

# Set the secret key for Flask application
app.secret_key = SECRET_KEY

# Create a PyMongo instance linked to the Flask app for database access
database = PyMongo(app)


# App routes

# 404 Error page
@app.errorhandler(404)
def page_not_found(error):
    """
    Handle a 404 error by rendering a custom 404 error page.

    This function is a Flask error handler for handling 404 errors. When a
    user accesses a route that does not exist, Flask will automatically
    call this function and return a custom 404 error page.

    Parameters:
    error (Exception): The exception that triggered the 404 error.

    Returns:
    tuple: A tuple containing the rendered HTML template for the 404 error
           page and the HTTP status code 404.
    """
    return render_template('404.html'), 404


# Home page
@app.route("/")
@app.route("/show_recipes")
def show_recipes():
    """
    Displays a list of recipes on the home page with sections for non-users.

    Returns:
        Flask.render_template: HTML template rendering the list of
        recipes and Non-user sections.
    """

    # Set active page
    active_page = "home"

    # Fetch the user's information from the session
    username = session.get("user")
    user = None
    if username:
        user = database.db.users.find_one({"username": username})
        recipes = database.db.recipes.find()

    else:
        recipes = (
            [recipe for recipe in database.db.recipes.aggregate(
                [{"$sample": {"size": 4}}])])

    return render_template(
        "recipes.html", recipes=recipes, user=user, active_page=active_page)


# Search recipes
@app.route("/search_recipes", methods=["POST"])
def search_recipes():
    """
    Search for recipes based on the provided search query.

    Returns:
        Flask.render_template: HTML template rendering the search results or
            redirecting to the "show recipes" page.
    """
    # Retrieve the search query from the form
    search_query = request.form.get("query")

    # Query the database to find recipes that match the search query
    recipes = list(database.db.recipes.find(
                    {"$text": {"$search": search_query}}))

    # Check if there are no search results
    if not recipes:
        flash("No results found. Please Try Again", "warning")
        return redirect(url_for("show_recipes"))

    return render_template("recipes.html", recipes=recipes, search=True)


# About page
@app.route("/about")
def about():
    """
    This function renders and displays the 'About' page.

    Returns:
        rendered HTML template for the About page.
    """

    # set active page
    active_page = "about"

    return render_template("about.html", active_page=active_page)


# sign up page
@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    """
    Handles user registration, performing various checks during the process.

     This route allows users to sign up by providing their personal
     information.
    It performs several checks, including:
    - Ensuring that passwords match.
    - Checking if the chosen username is available.
    - Verifying that the provided email is not already registered.

    If all checks pass, the user's information is stored securely, and they
    are redirected to the sign-in page.

    Returns:
        Flask.redirect: Redirects to the sign-in page after sign up complete.
        Flask.render_template: HTML template rendering the sign-up page.
    """

    # set active page
    active_page = "sign_up"

    if request.method == "POST":
        # check passwords match
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        # if passwords dont match return flash error message
        if password != confirm_password:
            flash("Passwords do not match, Please Try Again", "error")
            return redirect(url_for("sign_up"))
        # Check username is not already taken
        existing_user = database.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            flash("Username already in use, Please Try Again")
            return redirect(url_for("sign_up"))

        # Check if the email is already registered
        existing_email = database.db.users.find_one(
            {"email": request.form.get("email").lower()})
        if existing_email:
            flash("Email already registered, Please Try Again")
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
            "member_since": datetime.datetime.now(),
            "favorites": []
        }

        # Insert user document to database
        database.db.users.insert_one(register)

        # Display a flash message indicating successful sign-up,
        # request sign_in
        flash("Sign Up Successful! Please now Sign in with your credentials")
        return redirect(url_for("sign_in"))

    # Render the sign up page
    return render_template("sign_up.html", active_page=active_page)


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

    # set active page
    active_page = "sign_in"

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if authenticate_user(username, password):
            # redirect to show_recipes
            # change to url for profile when profile page built
            return redirect(url_for("show_recipes", username=session["user"]))
        else:
            flash("Incorrect Username and/or Password, Please Try Again")
            return redirect(url_for("sign_in"))

    # Render sign in page
    return render_template("sign_in.html", active_page=active_page)


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

    # set active page
    active_page = "profile"

    username = session.get("user")

    if username:
        user = database.db.users.find_one({"username": username})
        user_recipes_pack = database.db.recipes.find({"created_by": username})
        user_recipes = list(user_recipes_pack)
        favorite_recipes_pack = database.db.recipes.find(
            {"_id": {"$in": user["favorites"]}})
        favorite_recipes = list(favorite_recipes_pack)

        return render_template(
            "profile.html",
            user=user,
            user_recipes=user_recipes,
            favorite_recipes=favorite_recipes,
            active_page=active_page
        )
    else:
        # Handle case when the user is not in session
        flash("Error, Please sign in to access your profile.")
        return redirect(url_for("sign_in"))


# Edit profile page
@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    """
        Allows users to edit their profile information, including name, email,
        and password.

        This route provides a form for users to edit their profile information,
        including their first name, last name, email, and password. Users can
        update their profile details and change their password if desired.

        If the form is submitted with matching new passwords, the user's
        information is updated in the database, and they are redirected
        to their profile page. If the passwords do not match, an error message
        is displayed.

        Returns:
            Flask.redirect: Redirects to the user's profile page after
            successful profile update.
            Flask.render_template: HTML template rendering the edit profile
            form.

        """

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
            flash("Profile Updated Successfully")
            return redirect(url_for("profile"))
        else:
            flash("Passwords do not match. Please try again.", "error")

    # Render the edit profile form
    return render_template("edit_profile.html", user=user)


# Delete profile page
@app.route("/delete_profile", methods=["GET", "POST"])
def delete_profile():

    """
    Allows users to delete their profile.

    This route provides a confirmation form for users to delete their profile.
    Users are presented with a confirmation prompt before proceeding with
    profile deletion.

    If the form is submitted, the user's profile is deleted from the database,
    and they are logged out automatically. A flash message confirms the
    deletion.

    Returns:
        Flask.redirect: Redirects to a page after successful profile deletion.
        Flask.render_template: HTML template rendering the delete profile
        confirmation form.
    """

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
        return redirect(url_for("show_recipes"))

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
    - The 'Pillow' library for image manipulation.

    Note:
    - Function assumes  existence of 'database.db.recipes', for recipe storage.
    - It expects fields named 'recipe_name', 'category', 'recipe_description',
      'method_step[]', 'ingredient[]', and 'quantity[]', 'recipe_image'.
    - The 'recipe_image' field should contain recipe's image file for upload.
    - Image processing is done using Pillow to resize the image to 800x400
    while preserving the aspect ratio and cropping as needed.
    """

    if "user" not in session:
        flash("Error, You must be logged in to access this page.")
        return redirect(url_for("sign_in"))

    # set active page
    active_page = "add_recipe"

    if request.method == "POST":
        recipe_name = request.form.get("recipe_name")
        category = request.form.get("category")
        recipe_description = request.form.get("recipe_description")
        prep_time = request.form.get("prep_time")
        cook_time = request.form.get("cook_time")
        servings = request.form.get("servings")
        created_by = session["user"]
        ingredients = []
        method_step = request.form.getlist("method_step[]")
        date_added = datetime.datetime.now()
        formatted_date = date_added.strftime('%Y-%m-%d')
        admin_description = request.form.get("admin_description")
        product_link = request.form.get("product_link")
        product_text = request.form.get("product_text")
        product_image = request.form.get("product_image")

        # Upload the image to Cloudinary
        image_file = request.files["recipe_image"]
        if image_file:
            # Open the image using Pillow
            image = Image.open(image_file)

            desired_width = 800
            desired_height = 400
            original_width, original_height = image.size

            # Calculate the aspect ratios
            aspect_ratio = desired_width / desired_height
            original_aspect_ratio = original_width / original_height

            if original_aspect_ratio > aspect_ratio:
                # Crop the width to fit the aspect ratio
                new_width = int(desired_height * original_aspect_ratio)
                image = image.resize((new_width, desired_height))
                left = (new_width - desired_width) / 2
                right = (new_width + desired_width) / 2
                image = image.crop((left, 0, right, desired_height))
            else:
                # Crop the height to fit the aspect ratio
                new_height = int(desired_width / original_aspect_ratio)
                image = image.resize((desired_width, new_height))
                top = (new_height - desired_height) / 2
                bottom = (new_height + desired_height) / 2
                image = image.crop((0, top, desired_width, bottom))

            # Convert the image to WebP format
            output = io.BytesIO()
            image.save(output, format='WebP')
            image_file = io.BytesIO(output.getvalue())
            image_file.seek(0)

            # Upload the modified image to Cloudinary
            upload_result = upload(
                image_file, transformation={"crop": "fill"})
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
            "prep_time": prep_time,
            "cook_time": cook_time,
            "servings": servings,
            "image": image_url,
            "created_by": created_by,
            "date_added": formatted_date,
            "ingredients": ingredients,
            "method_step": method_step,
            "admin_description": admin_description,
            "product_link": product_link,
            "product_text": product_text,
            "product_image": product_image
            }

        database.db.recipes.insert_one(recipe)
        flash("Recipe Successfully Posted")
        return redirect(url_for("show_recipes"))

    categories = database.db.categories.find().sort("category", 1)
    return render_template(
        "add_recipe.html", categories=categories, active_page=active_page)


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

    # Fetch the user's information from the session
    username = session.get("user")
    user = None
    if username:
        user = database.db.users.find_one({"username": username})

    # Render the recipe details template and pass the recipe data
    return render_template("recipe_details.html", recipe=recipe, user=user)


@app.route("/delete_recipe/<recipe_id>", methods=["GET", "POST"])
def delete_recipe(recipe_id):
    """
    Allows users to delete a recipe if they have the necessary permissions.

    This route handles the deletion of a recipe. It checks whether the user is
    authenticated and has the appropriate permissions to delete the recipe.

    If the user is authenticated and authorized to delete the recipe, the
    function deletes the recipe's image from Cloudinary (if present),
    removes the recipe from the database, and provides a flash message
    confirming the deletion.

    If the user is not authorized to delete the recipe, An error message is
    displayed.

    Args:
        recipe_id (str): The unique identifier of the recipe to be deleted.

    Returns:
        Flask.redirect: Redirects to user's profile page after successful
        recipe deletion.
        Flask.render_template: HTML template rendering an error message if the
        user lacks the necessary permissions.
    """

    # Check if the user is authenticated
    if "user" not in session:
        flash("Error, Please sign in to delete a recipe.")
        return redirect(url_for("sign_in"))

    # Fetch the recipe details from the database using the recipe_id
    recipe = database.db.recipes.find_one({"_id": ObjectId(recipe_id)})

    # Check if the user is either the creator of the recipe or an admin
    if recipe and (
            recipe["created_by"] == session[
                "user"] or session["user"] == "admin"):

        # Delete the recipe image from Cloudinary
        if "image" in recipe:
            image_url = recipe["image"]
            # Extract public_id from the image URL
            public_id = image_url.split("/")[-1].split(".")[0]
            # Delete the image from Cloudinary
            cloudinary.api.delete_resources(public_id)

        # Delete the recipe from the database
        database.db.recipes.delete_one({"_id": ObjectId(recipe_id)})
        flash("Recipe successfully deleted.")
        return redirect(url_for("profile"))
    else:
        flash("Error, You do not have permission to delete this recipe.")
        return redirect(url_for("profile"))


# Edit recipe page
@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    """
    Edit an existing recipe in the database.

    If the method is GET, it retrieves the recipe details from the
    database and renders the 'edit_recipe.html' template with the
    existing data. If the method is POST, it updates the recipe with
    the new data from the form.

    Parameters:
    - recipe_id (str): The unique identifier for the recipe to edit.

    Returns:
    GET Request:
        - Render 'edit_recipe.html' template with the existing recipe data.

    POST Request:
        - If successful, flash message, redirect to 'show_recipes' page.
        - Validation errors, render 'edit_recipe.html' with error messages.

    Dependencies:
    - The 'request' object from Flask to access form data.
    - The 'session' object to access the current user's information.
    - The 'database' object to interact with the database.
    - The 'upload' function to upload the updated recipe image to Cloudinary.
    - The 'Pillow' library for image manipulation.

    Note:
    - Function assumes existence of 'database.db.recipes' for recipe storage.
    - It expects fields named 'recipe_name', 'category', 'recipe_description',
      'method_step[]', 'ingredient[]', and 'quantity[]', 'recipe_image'.
    - The 'recipe_image' field should contain the updated recipe's
    image file for upload.
    - Image processing is done using Pillow to resize the image to 800x400
    while preserving the aspect ratio and cropping as needed.
    """

    # Check if the user is authenticated
    if "user" not in session:
        flash("Error, Please sign in to edit a recipe.")
        return redirect(url_for("sign_in"))

    # Fetch the existing recipe details from the database using the recipe_id
    recipe = database.db.recipes.find_one(
            {"_id": ObjectId(recipe_id)})

    # Check if the user is the creator of the recipe or is admin
    if recipe and (
            recipe["created_by"] == session[
                "user"] or session["user"] == "admin"):

        if request.method == "POST":
            # Extract updated recipe information from the submitted form
            recipe_name = request.form.get("recipe_name")
            category = request.form.get("category")
            recipe_description = request.form.get("recipe_description")
            prep_time = request.form.get("prep_time")
            cook_time = request.form.get("cook_time")
            servings = request.form.get("servings")
            prep_time = request.form.get("prep_time")
            ingredients = []
            method_step = request.form.getlist("method_step[]")
            admin_description = request.form.get("admin_description")
            product_link = request.form.get("product_link")
            product_text = request.form.get("product_text")
            product_image = request.form.get("product_image")

            # Init image_url with existing img URL, None if no image is set
            image_url = recipe.get("image")

            # Check if a new image file has been uploaded
            image_file = request.files["image"]
            if image_file:
                # Open the image using Pillow
                image = Image.open(image_file)

                desired_width = 800
                desired_height = 400
                original_width, original_height = image.size

                # Calculate the aspect ratios
                aspect_ratio = desired_width / desired_height
                original_aspect_ratio = original_width / original_height

                if original_aspect_ratio > aspect_ratio:
                    # Crop the width to fit the aspect ratio
                    new_width = int(desired_height * original_aspect_ratio)
                    image = image.resize((new_width, desired_height))
                    left = (new_width - desired_width) / 2
                    right = (new_width + desired_width) / 2
                    image = image.crop((left, 0, right, desired_height))
                else:
                    # Crop the height to fit the aspect ratio
                    new_height = int(desired_width / original_aspect_ratio)
                    image = image.resize((desired_width, new_height))
                    top = (new_height - desired_height) / 2
                    bottom = (new_height + desired_height) / 2
                    image = image.crop((0, top, desired_width, bottom))

                # Convert the image to WebP format
                output = io.BytesIO()
                image.save(output, format='WebP')
                image_file = io.BytesIO(output.getvalue())
                image_file.seek(0)

                # Upload the modified image to Cloudinary
                upload_result = upload(
                    image_file, transformation={"crop": "fill"})
                image_url = upload_result["secure_url"]

            for i in range(len(request.form.getlist("ingredient[]"))):
                ingredient = {
                    "name": request.form.getlist("ingredient[]")[i],
                    "quantity": request.form.getlist("quantity[]")[i]
                }
                ingredients.append(ingredient)

            # Update the recipe details in the database
            database.db.recipes.update_one(
                {"_id": ObjectId(recipe_id)},
                {
                    "$set": {
                        "recipe_name": recipe_name,
                        "category": category,
                        "recipe_description": recipe_description,
                        "prep_time": prep_time,
                        "cook_time": cook_time,
                        "servings": servings,
                        "image": image_url,
                        "ingredients": ingredients,
                        "method_step": method_step,
                        "admin_description": admin_description,
                        "product_link": product_link,
                        "product_text": product_text,
                        "product_image": product_image
                    }
                }
            )
            flash("Recipe Successfully Updated")
            return redirect(url_for("show_recipes"))

        categories = database.db.categories.find().sort("category", 1)
        return render_template(
                "edit_recipe.html", recipe=recipe, categories=categories)
    else:
        flash("Error, You do not have permission to edit this recipe.")
        return redirect(url_for("profile"))


# Add a recipe to user favourites
@app.route("/add_to_favorites/<recipe_id>", methods=["POST"])
def add_to_favorites(recipe_id):
    """
    Add a recipe to the user's favorites.
    """
    username = session.get("user")

    if username:
        # Convert recipe_id to ObjectId
        recipe_id = ObjectId(recipe_id)
        # Check if the user has already added this recipe to their favorites
        user = database.db.users.find_one({"username": username})
        if recipe_id not in user["favorites"]:
            # Add the recipe ID to the user's favorites
            database.db.users.update_one(
                {"username": username}, {"$push": {"favorites": recipe_id}})
            flash("Recipe added to favorites successfully", "success")
        else:
            flash("Error, Recipe is already in your favorites", "warning")
    else:
        flash("Error, Please sign in to add recipes to your favorites.",
              "warning")

    return redirect(url_for("profile", recipe_id=recipe_id))


# Remove a recipe from user favourites
@app.route("/remove_favorite/<recipe_id>", methods=["POST"])
def remove_favorite(recipe_id):
    """
    Remove a recipe from the user's favorites.
    """
    username = session.get("user")

    if username:
        # Convert recipe_id to ObjectId
        recipe_id = ObjectId(recipe_id)

        # Check if the user has this recipe in their favorites
        user = database.db.users.find_one({"username": username})
        if recipe_id in user["favorites"]:
            # Remove the recipe ID from the user's favorites
            database.db.users.update_one(
                {"username": username}, {"$pull": {"favorites": recipe_id}})
            flash("Recipe removed from favorites successfully", "success")
        else:
            flash("Recipe is not in your favorites", "warning")
    else:
        flash("Please sign in to manage your favorites.", "warning")

    return redirect(url_for("show_recipes"))


# Manage categories page Admin only
@app.route("/manage_categories")
def manage_categories():
    """
    Allows administrator to manage recipe categories.
    """
    # Check the user's role (assuming the role is stored in a session variable)
    user = session.get("user")

    # Check if the user is an admin
    if user != "admin":
        # User is not an admin, handle unauthorized access
        flash("Error, Access Denied")
        return render_template("sign_in.html")

    # If the user is an admin, proceed with rendering the page
    active_page = "categories"

    categories = database.db.categories.find().sort("category", 1)
    return render_template(
        "manage_categories.html",
        categories=categories,
        active_page=active_page)


# Add a category form
@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    """
    Allows administrator to add a new recipe category.

    This route enables administrators to add a new recipe category by
    submitting a category name through a form. It checks if the category
    name already existsin the database and inserts the new category if
    it's unique.

    Returns:
        Flask.redirect: Redirects back to the manage categories page.
        Flash messages are displayed for category addition success or if the
        category already exists.
    """

    if request.method == "POST":
        # Get the category name from the form
        category_name = request.form.get("categoryName")

        # Check if the category name already exists in the database
        existing_category = database.db.categories.find_one(
                            {"category": category_name})

        if existing_category:
            flash("Error, Category already exists", "error")
        else:
            # Insert the new category into the database
            database.db.categories.insert_one({"category": category_name})
            flash("Category added successfully", "success")

    # Redirect back to the manage categories page
    return redirect(url_for("manage_categories"))


# Edit category form function
@app.route("/edit_category/<category_id>", methods=["POST"])
def edit_category(category_id):
    """
    Allows administrator to edit an existing recipe category.

    This route enables administrators to edit an existing recipe category by
    submitting an updated category name through a form. It updates the category
    in the database and provides a flash message confirming the update.

    Args:
        category_id (str): The unique identifier of the category to be edited.

    Returns:
        Flask.redirect: Redirects back to the "Manage Categories" page after
        the category is updated successfully.
        Flash messages are displayed to confirm the category update.

    Note:
        This route handles POST requests to update the category.
        GET requests are redirected to the "Manage Categories" page.
    """

    if request.method == "POST":
        # Get the updated category name from the form
        updated_category_name = request.form.get("updatedCategoryName")

        # Update the category in the database
        database.db.categories.update_one(
            {"_id": ObjectId(category_id)},
            {"$set": {"category": updated_category_name}}
        )
        flash("Category updated successfully", "success")

        # Redirect back to the "Manage Categories" page
        return redirect(url_for("manage_categories"))

    # Handle GET requests if needed
    return redirect(url_for("manage_categories"))


# Delete category route
@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    """
    Deletes a category based on the provided category_id.

    Args:
        category_id (str): The unique identifier of the category to delete.

    Returns:
        flask.Response: Redirects back to the "Manage Categories" page.
    """
    # Check if the user is an admin or has permission to delete categories
    if session.get("user") == "admin":
        # Delete the category from the database using its ID
        database.db.categories.delete_one({"_id": ObjectId(category_id)})
        flash("Category deleted successfully", "success")
    else:
        flash("Error, You do not have permission to delete categories",
              "error")

    # Redirect back to the "Manage Categories" page
    return redirect(url_for("manage_categories"))


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
