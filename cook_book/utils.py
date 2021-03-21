from __init__ import app
from flask_redis import FlaskRedis
redis_client = FlaskRedis(app)

def load_recipes(meal_name, recipe, ingredients, **kwargs):
    redis_client.set("meal_"+meal_name, recipe)
    for each_ingredients in ingredients:
        redis_client.sadd("ingredients_"+each_ingredients, meal_name)

    
