# What's fyyur?

Fyyur is simpley a website where you will find artists and venues in one place.

You can search for artists, add venues, add artists and even add shows for an artist in a venue.

The idea behind it is you can look at a venue and see who's playing there, or look at an artist and see their upcoming and past shows, or even look at the shows and see what time they start.

# More info about this project

This project is built using flask. It's one of the projects I did in a full stack course from udacity.

The end goal is to be able to demonstrate the fact that you can perform crud operations on a database.
Crud stands for create, read, update, delete.

# How to install?

Make sure to install the libraries found in the requirements.txt file and to have PostgreSQL installed first.
You also need to open the psql shell and create a database named fyyur with this command:
"CREATE DATABASE fyyur;".
After then from the terminal run these commands while being in the project folder:
flask db init
flask db migrate
flask db upgrade

This is to make sure that the database we created gets populated with the models in our code.

when you're done, run this command:
flask run
The app will launch, and then you can connect to the server from your browser with opening the url: localhost:5000

# Note

Overall, this is my first flask project. I come from a data science background and I confess, I really struggled with this project and to get it working.

You may or may not get some errors when running it, feel free to contribute if you find any.