import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)

app.SECRET_KEY = os.environ.get('SECRET_KEY')
app.config["MONGO_DBNAME"] = 'deeelish'
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["IMAGE_UPLOADS"] = "/workspace/deeelish/static/images/uploads/"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_image(filename):

    # We only want files with a . in the filename
    if not "." in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in ALLOWED_IMAGE_EXTENSIONS
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


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


@app.route('/insert_recipe', methods=['GET', 'POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    if request.method == "POST":
        file = request.files["file"]
        if file.filename == "":
            print("No filename")
            return redirect(request.url)
        if not allowed_image(file.filename):
            print("Image extension not allowed")
            return redirect(request.url)
        else:
            filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
        print("Image saved")
        return redirect(request.url)
    return redirect(url_for('get_recipes'))


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_meals_courses = mongo.db.meals_courses.find()
    all_cuisines = mongo.db.cuisines.find()
    return render_template('editrecipe.html', recipe=the_recipe, meals_courses=all_meals_courses, cuisines=all_cuisines)


@app.route('/update_recipe/<recipe_id>', methods=['GET', 'POST'])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    if request.method == "POST":
        file = request.files["file"]
        file.save(os.path.join(app.config["IMAGE_UPLOADS"], file.filename))
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


@app.route('/get_categories')
def get_categories():
    return render_template("categories.html",
    meals_courses=mongo.db.meals_courses.find().sort('meal_course_type'),
    cuisines=mongo.db.cuisines.find().sort('cuisine'))


@app.route('/edit_meal/<meal_id>')
def edit_meal(meal_id):
    return render_template('editmealcat.html',
            meal=mongo.db.meals_courses.find_one(
                {'_id': ObjectId(meal_id)}))


@app.route('/edit_cuisine/<cuis_id>')
def edit_cuisine(cuis_id):
    return render_template('editcuisinecat.html',
            cuis=mongo.db.cuisines.find_one(
                {'_id': ObjectId(cuis_id)}))


@app.route('/update_meal/<meal_id>', methods=['POST'])
def update_meal(meal_id):
    meals = mongo.db.meals_courses
    meals.update({'_id': ObjectId(meal_id)},
        {'meal_course_type': request.form.get('meal_course_type')})
    return redirect(url_for('get_categories'))


@app.route('/update_cuisine/<cuis_id>', methods=['POST'])
def update_cuisine(cuis_id):
    mongo.db.cuisines.update(
        {'_id': ObjectId(cuis_id)},
        {'cuisine': request.form.get('cuisine')})
    return redirect(url_for('get_categories'))


@app.route('/delete_meal/<meal_id>')
def delete_meal(meal_id):
    mongo.db.meals_courses.remove({'_id': ObjectId(meal_id)})
    return redirect(url_for('get_categories'))


@app.route('/delete_cuisine/<cuis_id>')
def delete_cuisine(cuis_id):
    mongo.db.cuisines.remove({'_id': ObjectId(cuis_id)})
    return redirect(url_for('get_categories'))


@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')


@app.route('/insert_meal', methods=['POST'])
def insert_meal():
    meal_doc = {'meal_course_type': request.form.get('meal_course_type')}
    mongo.db.meals_courses.insert_one(meal_doc)
    return redirect(url_for('get_categories'))


@app.route('/insert_cuisine', methods=['POST'])
def insert_cuisine():
    cuisine_doc = {'cuisine': request.form.get('cuisine')}
    mongo.db.cuisines.insert_one(cuisine_doc)
    return redirect(url_for('get_categories'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
