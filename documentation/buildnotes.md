Build notes 

Installed flask using pip3 install flask which also installs packages: werkzueg, blinker, click and itsdangerous 
created app.py file 
created env.py file to hold sensitive information the app requires 
ensure env.py and other sensitive files are included in the .gitignore file 
Add setdefaults in env.py 
add initial imports to app.py 
add flask app initialization with debug mode display test statement to test deploy 
use terminal command: pip3 freeze --local > requirements.txt to create and update the requirements.txt file for flask setup... requirements.txt lists the depedancies needed for flask
 use termianl command: echo web: python app.py > Procfile to create Procfile for flask setup 
 Remove extra blank line at end of Procfile as this may cause issues with Flask 
 created app on flask website and add deatails from env.py to the config vars in flask app settings
 Installed flask pymongo using command pip3 install flask-pymongo
Attempted to install dns python using command pip3 install dnspython but found it was already installed
Updated requrements.txt file using command  pip3 freeze --local > requirements.txt this is for heroku so it knows what is required to run the app.

mongo uri requried finding python version using command python --version 
update mongo uri on heroku app config
Create a PyMongo instance linked to the Flask app for database access
add needed imports from flask in app.py 
add a templates directory used by python to render pages. using command mkdir templates
add recipes.html and base.html using touch command  touch templates/base.html
add static directory for css images js etc
added database connection test code to display some basic data from the MongoDB
built basic base template
add external(materialize and fontawesome) and project stylesheets links in head of base 
add script tags for font awesome jquery materialize and custom script
create materialize navbar with mobile dropdown, style with css and functionality with JS. 
create sign up page using materialize stlying along with materialize form and buttons
built functionality from sign up form to database. had to import date time to the app.py file to store date user joined.
used werkzueg security to hash password to be stored onto the database.
added confirm password on sign up for good practice 
after sign up put user into session to be changed to request sign in when sign in built
built flash message display html, added to template and styled
deleted js function for checking passwords match and added it to the python sign_up function this was to achieve not seeing  the js alert message that appears in a pop-up form now after change it it a flash message that is rendered to display where all over flash messages display.
add sign_in.html build materialize sign in form with button
add sign in url for links to nav bar and at botom of signup and sign in for already signed up? and already a member?
build sign in functionality check if current user and check password.
Updated registration process: After successful registration, users are now redirected to the sign-in page with a success message
Add detailed doc string notes
add sign out functionality and links
build show recipes page using Materialize cards
Build basic profile page showing user details need to add edit option and my recipes section
Add functionality for profile page and add to navbar for user in session only
Sort nav bar for users in session and users not in session
updated profile page with edit profile button need to add edit functionality did try got stuck will return
Build welcome page as home page for users not in session this page is to encourage not members to join.
Build about page
Build basic add recipe form with styling and functional categorie dropdown using python to access categories db and jquery to initialize the drop down.
Add add ingriedient and add method step buttons to add_recipe form create functionality with jquery 
create add recipe form to db functionality 
styled add recipe card 
styled show recipes page so tiles have border to seperate background image display in rows of 2 large screen and list of tiles on screens smaller than ipad
found new colour scheme on pinterest by lookcolor.ru they didnt add the colour codes so i inserted the picture to adobe color and allowed that to pick the colours from the picture
added button effects to include colours from theme
create upload photo on recipe form required install cloudinary package usisng command pip install cloudinary, Add cloudinary imports to app.py,
Add cloudinary configurations to app.py
Add cloudinary config values to env.py and flask app configs
Update requirements.txt using command pip3 freeze --local > requirements.txt
Added python functionality to upload photo to cloudinary and store its url path to the database enabling me to use img src {{recipe.image}} to display image on recipe card. Need to look at recipe name and category posibly better with a backgroung for visibility.
Build basic view recipe page and functionality 
add recipe image to recipe_details page with styling and redponsiveness
Add recipe ingredients and steps to details page.
Styled recipe card images to display central so the photo is more eye catching
built edit profile page and functionality. nb. need to add icons to both profile and edit profile page
build delete profile page to confirm profile deletion and functionality to delete profile
add icons to edit profile page
add icons to profile page
updated structure of recipe_details page
re added prefill values on edit profile page
Add my users recipe section in my profile with edit and delete buttons
Added delete recipe function with features to check the user created the document they are trying to delete or if they are the user admin,
chose to have the delete recipe function also delete the image on cloudinary could change this if wanted to collect images.
copied add recipe page to create edit recipe page
build edit recipe functionality. had to retrieve the ingredients list as well as the method list. allowed admin to edit all,
build functionality in edit recipe to upload new image and delete old 
nb. issue to sort with text area creating tabbed space on reload instead of showing placeholder or value text.
Fixed issue with edit recipe function  not tottaly sure of the problem but I built from scratch i found the only difference with the working rebuild was how i updated the new recipe details to the database.
Add basic manage categories page and Admin navbar
Add add edit and delete category buttons.
Add add category form and functionality
Add Edit category form and functionality I chose for this all to be prefilled forms on the 1 page it keeps control in a central point and saved time building seperete html pages for each form.
Add Delete category button and functionality

Add search functionality required creating a search index achieved by: opening python interperator in console using command python3, import my database from my app.py using from app import database,
create search index including all fields from recipe the user is able to search using command:database.db.recipes.create_index([("recipe_name", "text"), ("category", "text"), ("recipe_description", "text"), ("created_by", "text")]) to then view the index in console use command:
 database.db.recipes.index_information() to delete all indexes use: database.db.recipes.drop_indexes()
quit python interperator using commad: quit()

built seartch recipe form and functionality added flash message and redirect for when no results are found.

Created Add to favourites Functionality had to add favourites field with empty array upon sign up for the favs to be added to.
Add favorites section to profile page and functionality to show user favorites. goit stuck due to needing convert recipe_id to an objectid(..) due to way it is stored in mongodb database.

Add remove favorite function and button
Add functionality so the user sees either the add to favorites or remove favorite buttons depending on wether they have the recipe as a favourite or not.

 

to research colour phycology in relation to restaurant and food brands at https://medium.com/@ashley_howell/understanding-colour-psychology-for-restaurants-brands-dbb7ffbcecae

research colours that influence food sales: https://jenndavid.com/colors-that-influence-food-sales-infographic/

Chose to go with greens and black and mushroom due to reasons researched and noted on notepad 

updated colour to show recipes and base, change colour and layout to recipe details page

edited recipes page due to layout issue
updated profile page colours and layout

update nav bar and fonts

update colour theme across site except welcome and about 

add paragrapgh for users with no uploaded recipes or favorites added.

rebuild welcome page new colors and added carousel

edit navbar to stick to top

create footer bar with links

nb
describe how the mongo URI connection as generated by mongo didn't include the database name which caused an issue in connecting to the database, but the fix was to add the database name to the URI and then you were able to retrieve your recipes. TESTING BUGS
font research from https://www.pagecloud.com/blog/best-google-fonts-pairings chose fast hand for logo only. playfair display for titels and alice for text. wanted elegant almost hand written yet clear but prettier than typed style fonts.