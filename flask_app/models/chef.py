import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')


class Chef:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []
        self.favorites = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO chefs (email, first_name, last_name, password) VALUES (%(email)s, %(first_name)s, %(last_name)s, %(password)s);"
        return connectToMySQL("recipes").query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM chefs;"
        results = connectToMySQL('recipes').query_db(query)
        chefs = []
        for row in results:
            chefs.append( cls(row) )
        return chefs

    @classmethod
    def get_chef(cls,data):
        query = "SELECT * FROM chefs where id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query,data)
        chef = []
        for row in results:
            chef.append( cls(row) )
        return chef

    @classmethod
    def get_chef_by_email(cls, data):
        query = "SELECT * FROM chefs where email = %(email)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        for row in results:
            return row 

    @classmethod
    def get_chef_recipes(cls, data):
        query = "SELECT * FROM chefs LEFT JOIN recipes ON recipes.chef_id = chefs.id WHERE chefs.id = %(id)s;"
        results = connectToMySQL('recipes').query_db( query , data ) 
        chef_with_recipes = cls( results[0] )
        for row in results:
            recipe_data = {
                "id" : row["recipes.id"],
                "name" : row["name"],
                "description" : row["description"],
                "instructions" : row["instructions"],
                "cooking_time" : row["cooking_time"],
                "made_on" : row["made_on"],
                "created_at" : row["recipes.created_at"],
                "updated_at" : row["recipes.updated_at"],
                "chef_id": row['chef_id']
            }
            chef_with_recipes.recipes.append( recipe.Recipe( recipe_data ) )
        return chef_with_recipes

    @staticmethod
    def validate_signup( data ):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        if not NAME_REGEX.match(data['first_name']): 
            flash("Invalid First Name!")
            is_valid = False
        if len(data['first_name']) < 2: 
            flash("First Name too short!")
            is_valid = False
        if not NAME_REGEX.match(data['last_name']): 
            flash("Invalid Last Name!")
            is_valid = False
        if len(data['last_name']) < 2: 
            flash("Last Name too short!")
            is_valid = False
        if data['confirm'] != data['password']:
            flash("Passwords DO NOT match")
            is_valid = False
        if len(data['password']) <= 8: 
            flash("Invalid Password!")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_signin( data ):
        is_valid = True
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(data['password']) < 8: 
            flash("Invalid Password!")
            is_valid = False
        return is_valid

    @classmethod
    def get_chefs_favorites( cls , data ):
        query = "SELECT * FROM chefs LEFT JOIN favorites ON favorites.chef_id = chefs.id LEFT JOIN recipes ON favorites.recipe_id = recipes.id WHERE chefs.id = %(id)s;"
        results = connectToMySQL('recipes').query_db( query , data ) 
        chef = cls( results[0] )
        for row in results:
            recipe_data = {
                "id" : row["recipes.id"],
                "name" : row["name"],
                "description" : row["description"],
                "instructions" : row["instructions"],
                "cooking_time" : row["cooking_time"],
                "made_on" : row["made_on"],
                "created_at" : row["recipes.created_at"],
                "updated_at" : row["recipes.updated_at"],
                "chef_id": row['chef_id']
            }
            chef.favorites.append( recipe.Recipe( recipe_data ) )
        return chef


    @classmethod
    def deletelike(cls,data):
        query = "DELETE FROM favorites WHERE recipe_id = %(recipe_id)s and chef_id = %(chef_id)s"
        return connectToMySQL('recipes').query_db(query, data)
