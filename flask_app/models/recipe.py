from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models import chef
bcrypt = Bcrypt(app)



class Recipe:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.cooking_time = data['cooking_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.chef_id = data['chef_id']
        self.likes = []

    @classmethod
    def save( cls , data ):
        query = "INSERT INTO recipes ( name, description, instructions, cooking_time, made_on, chef_id ) VALUES (%(name)s, %(description)s, %(instructions)s, %(cooking_time)s, %(made_on)s, %(chef_id)s );"
        return connectToMySQL('recipes').query_db( query, data )

    @classmethod
    def update( cls , data ):
        query = "UPDATE recipes SET  name = %(name)s, description = %(description)s, instructions = %(instructions)s, cooking_time = %(cooking_time)s, made_on =  %(made_on)s, chef_id = %(chef_id)s where recipes.id = %(id)s;"
        return connectToMySQL('recipes').query_db( query, data )

    @classmethod
    def get_recipe(cls, data):
        query = "SELECT * FROM recipes where id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        return results[0]

    @classmethod
    def get_recipe_by_name(cls, data):
        query = "SELECT * FROM recipes where name = %(name)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        for row in results:
            return row

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes WHERE recipes.id = %(id)s"
        return connectToMySQL('recipes').query_db(query, data)

    @staticmethod
    def validate_recipe( data ):
        is_valid = True
        if len(data['name']) < 2: 
            flash("Name not Valid!")
            is_valid = False
        if len(data['description']) < 2: 
            flash("Description too short!")
            is_valid = False
        if len(data['instructions']) < 2: 
            flash("Instructions too short!")
            is_valid = False
        return is_valid


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL('recipes').query_db(query)
        recipes = []
        for recipe in results:
            recipes.append( cls(recipe) )
        return recipes

    @classmethod
    def likerecipe( cls , data ):
        query = "INSERT INTO favorites (recipe_id, chef_id ) VALUES (%(recipe_id)s, %(chef_id)s);"
        return connectToMySQL('recipes').query_db( query, data )

    @classmethod
    def how_many_liked( cls , data ):
        query = "SELECT * FROM recipes LEFT JOIN favorites ON favorites.recipe_id = recipes.id LEFT JOIN chefs ON favorites.chef_id = chefs.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL('recipes').query_db( query , data ) 
        recipes = cls( results[0] )
        for row in results:
            chef_data = {
                "id" : row['id'],
                "first_name": row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "created_at" : row['created_at'],
                'updated_at' : row['updated_at']
            }
            recipes.likes.append( chef.Chef( chef_data ) )
        return recipes

    @classmethod
    def get_recipe_by_like(cls, data):
        query = "SELECT * FROM favorites where recipe_id = %(id)s;"
        results = connectToMySQL('recipes').query_db(query, data)
        for row in results:
            return row