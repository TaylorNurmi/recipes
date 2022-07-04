from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.chef import Chef
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    if 'chef_id' in session:
        data = {
            "id": session["chef_id"]
        }
        myrecipes = Chef.get_chef_recipes(data)
        favorite_recipes = Chef.get_chefs_favorites(data)
        return render_template("dashboard.html", myrecipes = myrecipes, favorite_recipes = favorite_recipes)
    else:
        return redirect('/')


@app.route('/signup', methods = ['Post'])
def signup():
    data = { 
        "email" : request.form["email"] 
        }
    chef_exists = Chef.get_chef_by_email(data)
    if chef_exists:
        flash("email already in use")
        return redirect("/")
    if not Chef.validate_signup(request.form):
        return redirect('/')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "email": request.form["email"],
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "password": pw_hash,
            "confirm": request.form["confirm"]
        }
        chef_id = Chef.save(data)
        session['chef_id'] = chef_id
        session['chef_name'] = request.form["first_name"]
    return redirect("/dashboard")

@app.route('/login', methods=['POST'])
def login():
    data = { 
        "email" : request.form["email"] 
        }
    chef_exists = Chef.get_chef_by_email(data)
    if not chef_exists:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(chef_exists['password'], request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['chef_id'] = chef_exists['id']
    session['chef_name'] = chef_exists['first_name']
    return redirect("/dashboard")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route("/deletelike/<int:id>")
def deletelike(id):
    data = {
        "recipe_id": id,
        "chef_id": session['chef_id']
    }
    Chef.deletelike(data)
    return redirect("/dashboard")