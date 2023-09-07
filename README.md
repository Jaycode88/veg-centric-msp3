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

nb
describe how the mongo URI connection as generated by mongo didn't include the database name which caused an issue in connecting to the database, but the fix was to add the database name to the URI and then you were able to retrieve your recipes. TESTING BUGS
font research from https://www.pagecloud.com/blog/best-google-fonts-pairings chose fast hand for logo only. playfair display for titels and alice for text. wanted elegant almost hand written yet clear but prettier than typed style fonts.