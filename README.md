The App is written in Python using FLask framework and to store data i am using Redis

Files and folder structure:
    cook_book/help_me_cook.py --> contains the view functions of MVC framework
    cook_book/recipe.py --> contains the recipe class to load, retrive from Redis DB
    requirement.txt --> contains python dependencies for the application
    static --> contains css/js files
    templates --> contains html files to render

Dependencies:
    System packages: python 2.7
    Application packages: Flask, Request Library, Redis connector

To install depencies:
    From the command line "./run_install.sh install"

To run the application:
    from the command line "./run_install.sh run"

API supported:
    load -->
            1) syntax --> http://127.0.0.1:5000/load?query=https://www.themealdb.com/api/json/v1/1/random.php
    search --> 
            1) syntax --> http://127.0.0.1:5000/given_ingredients?ingredients=butter
            2) suuports search by partial ingredients in a recipe     

HTML pages
    1) Home page --> contains input box to load the queries
    2) result page --> search result page --> To view search recipe by ingredients

    
