from flask_app import app
from flask import render_template, session, redirect, flash, request
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Must be logged in!")
        return redirect("/")
    data = {
        "user_id" : session["user_id"]
    }
    user_recipes = User.get_user_recipes(data)
    return render_template("dashboard.html", user_recipes=user_recipes)



@app.route("/logout")
def logout():
    session.clear()
    flash("logged out!")
    return render_template("index.html")



@app.route("/delete/<int:id>")
def delete_recipe():    
    data = {
        "id":id
    }
    Recipe.delete_recipe(data)
    return redirect("/dashboard")



@app.route("/create")
def create():
    return render_template("create.html")



@app.route("/create/recipe", methods=["POST"])
def save():

    if "user_id" not in session:
        flash("Must be logged in!")
        return redirect("/")

    if Recipe.validate_recipe(request.form):
         data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "date_made": request.form["date_made"],
            "under30": request.form["under30"],
            "user_id": session["user_id"]
         }
         Recipe.save(data) 
         return redirect("/dashboard")
    else:
    
        return redirect("/create")

@app.route("/edit/<int:id>")
def edit(id):
    data = {
        "id": id
    }
    recipe = Recipe.get_by_id(data)
    return render_template("editrecipe.html", recipe=recipe)


@app.route("/editrecipe", methods = ["POST"])
def edit_recipe():
    if "user_id" not in session:
        flash("Must be logged in!")
        return redirect("/")
    print("we made it")
    
    if Recipe.validate_recipe(request.form):
         data = {
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "date_made": request.form["date_made"],
            "under30": request.form["under30"],
            "user_id": session["user_id"]
         }
         Recipe.update(data) 
         return redirect("/dashboard")
    else:
    
        return redirect("/editrecipe")


@app.route("/recipe/instructions/<int:id>")
def showrecipe(id):
        data = {
        "id": id
    }
    

