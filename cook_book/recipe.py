from __init__ import app
from flask_redis import FlaskRedis
redis_client = FlaskRedis(app)


class Recipe:
    def __init__(self):
        pass

    def load_from_json(self, **payload):
        self.name = payload["strMeal"].lower()
        self.instructions = payload["strInstructions"]
        self.ingredients = list()
        i = 1
        while(1):
            if "strIngredient" + str(i) in payload.keys():
                if payload["strIngredient" + str(i)] and not payload["strIngredient" + str(i)] == "":
                    self.ingredients.append(payload["strIngredient" + str(i)].replace(",", "").lower())
            else:
                break
            i += 1

    def save(self):
        self.__save_recipe()        
        self.__create_index_on_ingredients()

    def __save_recipe(self):
        redis_client.hset(self.__encode(self.name), "instructions", self.instructions)
        redis_client.hset(self.__encode(self.name), "ingredients", ",".join(self.ingredients))
        redis_client.hset(self.__encode(self.name), "name", self.name)

    def __create_index_on_ingredients(self):
        for each_ingredients in self.ingredients:
            redis_client.sadd("__ingredients_"+self.__encode(each_ingredients), self.name)

    def __get_recipe(self, name):
        return redis_client.hget(name)

    def __encode(self, field):
        return field.lower().replace(" ","_")
    
    def __decode(self, field):
        return field.lower().replace("_", " ")


class Recipes:
    def __init__(self):
        pass
    
    def get_all_recipes(self, ingredients):
        full_matched_recipes = dict()
        partial_matched_recipes = dict()
        for each_ingredient in ingredients:
            recipe_names = redis_client.smembers("__ingredients_" + self.__encode(each_ingredient))
            for each_recipe_name in recipe_names:
                recipe = self.get_recipe(each_recipe_name)
                if not each_recipe_name in full_matched_recipes.keys() and self.check_if_ingredients_belong(recipe, ingredients):
                    full_matched_recipes[each_recipe_name] = recipe
                else:
                    partial_matched_recipes[each_recipe_name] = recipe
        return full_matched_recipes.values(), partial_matched_recipes.values()
    
    def get_recipe(self, recipe_name):
        recipe = redis_client.hgetall(self.__encode(recipe_name))
        recipe["instructions"] = recipe["instructions"].decode('utf-8')
        recipe["name"] = recipe["name"].decode('utf-8')
        recipe["ingredients_list"] = set([each.decode('utf-8') for each in recipe["ingredients"].split(",")])  
        return recipe

    def check_if_ingredients_belong(self, recipe, ingredients):
        recipe_ingredients = set(recipe["ingredients"].split(","))
        for each_recipe_ingredient in recipe_ingredients:
            if not self.__encode(each_recipe_ingredient) in ingredients:
                return False
        else:
            return True

    def __encode(self, field):
        return field.lower().replace(" ","_")
    
    def __decode(self, field):
        return field.lower().replace("_", " ") 
