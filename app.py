import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
  import env 

app = Flask(__name__)

app.SECRET_KEY = os.environ.get('SECRET_KEY')
app.config["MONGO_DBNAME"] = 'deeelish'
app.config["MONGO_URI"] = os.getenv("MONGO_URI")


mongo = PyMongo(app)


@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", recipes=mongo.db.recipes.find())


@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    recipes = mongo.db.recipes
    the_recipe = recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('viewrecipe.html', recipe=the_recipe)


@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html',
            meals_courses=mongo.db.meals_courses.find(),
            cuisines=mongo.db.cuisines.find())


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_meals_courses = mongo.db.meals_courses.find()
    all_cuisines = mongo.db.cuisines.find()
    return render_template('editrecipe.html', recipe=the_recipe, meals_courses=all_meals_courses, cuisines=all_cuisines)


@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update({'_id': ObjectId(recipe_id)},
        {
            'add_photo': request.form.get('add_photo'),
            'recipe_name': request.form.get('recipe_name'),
            'recipe_description': request.form.get('recipe_description'),
            'meal_course_type': request.form.get('meal_course_type'),
            'cuisine': request.form.get('cuisine'),
            'serves': request.form.get('serves'),
            'time': request.form.get('time'),
            'is_vegetarian': request.form.get('is_vegetarian'),
            'is_vegan': request.form.get('is_vegan'),
            'is_glutenFree': request.form.get('is_glutenFree'),
            'is_dairyFree': request.form.get('is_dairyFree'),
            'add_ingredients': request.form.get('add_ingredients'),
            'method': request.form.get('method')
        })
    return redirect(url_for('get_recipes'))


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
