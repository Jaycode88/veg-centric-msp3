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



nb
describe how the mongo URI connection as generated by mongo didn't include the database name which caused an issue in connecting to the database, but the fix was to add the database name to the URI and then you were able to retrieve your recipes. TESTING BUGS
font research from https://www.pagecloud.com/blog/best-google-fonts-pairings chose fast hand for logo only. playfair display for titels and alice for text. wanted elegant almost hand written yet clear but prettier than typed style fonts.