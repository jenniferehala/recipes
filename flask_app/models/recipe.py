from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
import re

class Recipe:
    def __init__(self,data):
        self.id = data["id"]
        self.name = data ["name"]
        self.description = data["description"]
        self.instructions = data ["instructions"]
        self.under30 = data["under30"]
        self.date_made = data["date_made"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]


    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe["name"]) < 3:
            flash("Recipe name needs to be more than 3 characters")
            is_valid = False
        if len(recipe["description"]) < 3:
            flash("description needs letter")
            is_valid = False
        if len(recipe["instructions"]) < 3:
            flash("instructions needs letter")
            is_valid = False
        if len(recipe["date_made"]) < 1:
            flash("date needs to be entered")
            is_valid = False    
        if "under30" not in recipe:
            flash("Enter under 30 or not!")
            is_valid = False

        return is_valid

    @classmethod
    def delete_recipe(cls,data):
        query="DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL('recipes_db').query_db(query,data)
    
    @classmethod
    def save(cls,data):
        query="INSERT INTO recipes (name,description,instructions,date_made,under30,user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under30)s, %(user_id)s);"
        return connectToMySQL("recipes_db").query_db(query,data)
    
    @classmethod
    def get_by_id(cls,data):
        query="SELECT * FROM recipes WHERE id = %(id)s"
        recipe = connectToMySQL("recipes_db").query_db(query,data)
        return cls(recipe[0])
    
    @classmethod
    def update(cls,data):
        query ="UPDATE recipes SET name = %(name)s, description=%(description)s, instructions=%(instructions)s, date_made =%(date_made)s, under30 = %(under30)s WHERE id = %(id)s;" 
        return connectToMySQL("recipes_db").query_db(query,data)