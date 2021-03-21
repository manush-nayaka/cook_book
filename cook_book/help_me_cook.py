import requests
import json
import logging
from flask import escape, request, render_template
from utils import load_recipes
from recipe import Recipe, Recipes
from __init__ import app



@app.route('/')
def home():
    return render_template("home.html")


@app.route("/load")
def load():
    try:
        query = request.args["query"]
        logging.info("Requesting from MealDB with query {}".format(query))
        res = requests.get(query)
        meals = res.json().get("meals", [])
        loaded_recipes = []
        if res.status_code == 200:
            for each_meal in meals:
                recipe = Recipe() 
                recipe.load_from_json(**each_meal)
                recipe.save()
                loaded_recipes.append(recipe)
            return render_template("home.html", loaded_recipes=loaded_recipes, query=query)
        else:
            return "<h4>MealDB query returned with response code {}, with message </h4>{}".format(res.status_code, res.text)
    except requests.exceptions.ConnectionError:
        logging.error("connection error")
        return "Could not make contact with MealDB server"
    except requests.exceptions.Timeout:
        logging.error("timed out")
        return "Request to MealDB timed out"
    except requests.exceptions.RequestException as e:
        logging.error("Error: {}".format(e))
        return "Something happened check logs"


@app.route("/given_ingredients")
def given_ingredients():
    try:
        #ingredients = set(request.args["ingredients"].split(","))
        ingredients = set([each.strip() for each in request.args["ingredients"].split(",")])
        recipes = Recipes()
        full_match, partial_match = recipes.get_all_recipes(ingredients)
        return render_template("searched_recipes.html",full_match=full_match, partial_match=partial_match, ingredients=ingredients)
    except requests.exceptions.RequestException as e:
        logging.error("Error: {}".format(e))
        return "Something happened check logs"


if __name__ == "__main__":
    if app.debug:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    else:
        logging.basicConfig(filename='example.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)
    app.run(host='0.0.0.0')
