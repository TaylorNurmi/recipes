from flask import Flask, render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.recipe import Recipe

@app.route('/recipes/<int:id>')
def recipe(id):
    count = 0
    data = {
        "id": id
    }
    recipe_likes = Recipe.get_recipe_by_like(data)
    recipes = Recipe.get_recipe(data)
    likes = Recipe.how_many_liked(data)
    if recipe_likes:
        for like in likes.likes:
            count += 1
        return render_template("recipes.html", id = id, recipes = recipes, count = count)
    else:
        return render_template("recipes.html", id = id, recipes = recipes, count = count)

@app.route('/newrecipes')
def newrecipe():
    return render_template("newrecipes.html")

@app.route('/addrecipes', methods = ['Post'])
def addrecipe():
    data = { 
        "name" : request.form["name"] 
        }
    recipe_exists = Recipe.get_recipe_by_name(data)
    if recipe_exists:
        flash("Recipe Already exists")
        return redirect("/newrecipes")
    if not Recipe.validate_recipe(request.form):
        return redirect("/newrecipes")
    else:
        data = {
            "chef_id": session["chef_id"],
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "cooking_time": request.form["cooking_time"],
            "made_on": request.form["made_on"]
        }
        Recipe.save(data)
        return redirect("/dashboard")

@app.route('/updaterecipes', methods = ['Post'])
def updaterecipe():
    id = session['recipe_id']
    if not Recipe.validate_recipe(request.form):
        return redirect(url_for('editrecipe', id = session['recipe_id']))
    else:
        data = {
            "id": id,
            "chef_id": session["chef_id"],
            "name": request.form["name"],
            "description": request.form["description"],
            "instructions": request.form["instructions"],
            "cooking_time": request.form["cooking_time"],
            "made_on": request.form["made_on"]
        }
        Recipe.update(data)
        return redirect("/dashboard")

@app.route('/editrecipes/<int:id>')
def editrecipe(id):
    data = {
        "id": id
    }
    session['recipe_id'] = id
    recipes = Recipe.get_recipe(data)
    return render_template("editrecipes.html", id = id, recipes = recipes)


@app.route("/delete/<int:id>")
def delete(id):
    data = {
        "id": id
    }
    Recipe.delete(data)
    return redirect("/dashboard")



@app.route('/allrecipes')
def allrecipes():
    recipes = Recipe.get_all()
    return render_template("allrecipes.html", recipes = recipes)


@app.route('/like', methods = ['Post'])
def likerecipe():
    data = { 
        "recipe_id" : request.form["id"],
        "chef_id": session["chef_id"]
        }
    Recipe.likerecipe(data)
    return redirect("/dashboard")









