from flask_app import app
from flask import render_template, flash, redirect, request, session
from flask_app.models.recipe import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registration", methods=["POST"])
def register():

    if User.reg_valid(request.form):
        
        pw_hash = bcrypt.generate_password_hash(request.form["password"])
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "confirm_pass": request.form["confirm_pass"],
            "password": pw_hash
        }

        user_id = User.save(data) #INSERT INTO returns id, user_id is equal to the newly created user 
        session["user_id"] = user_id #put that newly created user inside of session
        flash("User created")

        return redirect("/")
    else:
        return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    data = {                                   # pull email from form, two step process
        "email": request.form["email"]         # check in email exists, then verify password
    }
    user_in_db = User.get_by_email(data)       #user_in_db is like a question, get by email grabs the user dictionary

    if not user_in_db:                         #user not in db
        flash("Invalid Email/Password")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid Email/Password")
        return redirect ("/")
    
    session["user_id"] = user_in_db.id        #grab id from db, it will give us id of user that logged in and set it into session
    session["first_name"] = user_in_db.first_name
    session["email"] = user_in_db.email
    return redirect("/dashboard")




# @app.route("/edit", methods=["POST"])
# def edit_recipe(id):
#     data = {
#         "id":id
#     }
#     User.get_recipe(data)

# return render_template("editrecipe.html")


