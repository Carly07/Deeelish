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


#---------Index Page---------------------

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


#---------Tips & Techniques Page---------------------

@app.route('/tips_technique')
def tips_technique():
    return render_template("tips.html")


#---------Discover Recipes Page Functionality---------------------

@app.route('/get_recipes')
def get_recipes():

#---------------Filter Function------------------

    filter = {}
    suitability = request.args.get('suitability')
    if suitability == 'vegetarian':
        filter['is_vegetarian'] = True
    elif suitability == 'vegan':
        filter['is_vegan'] = True
    elif suitability == 'gluten':
        filter['is_glutenFree'] = True
    elif suitability == 'dairy':
        filter['is_dairyFree'] = True
    print(filter)
    if filter:
        recipes = mongo.db.recipes.find(filter)
        meal_course_types = [mct for mct in mongo.db.meals_courses.find({}, {"meal_course_type": 1})]
        cuisines = [cuisine for cuisine in mongo.db.cuisines.find({}, {"cuisine": 1})]
    else:
        recipes=mongo.db.recipes.find()
        meal_course_types = [mct for mct in mongo.db.meals_courses.find({}, {"meal_course_type": 1})]
        cuisines = [cuisine for cuisine in mongo.db.cuisines.find({}, {"cuisine": 1})]
    return render_template("recipes.html", recipes=recipes, meal_course_types=meal_course_types, cuisines=cuisines)


#---------View Recipe Page Functionality---------------------

@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    recipes = mongo.db.recipes
    the_recipe = recipes.find_one({"_id": ObjectId(recipe_id)})
    meal_name = mongo.db.meals_courses.find_one(
        {"_id": ObjectId(the_recipe.get("meal_course_type"))})["meal_course_type"]
    cuisine_name = mongo.db.cuisines.find_one(
        {"_id": ObjectId(the_recipe.get("cuisine"))})["cuisine"]
    return render_template('viewrecipe.html', recipe=the_recipe,
                           cuisine=cuisine_name, meal_course_type=meal_name)


#---------Add Recipe Page Functionality---------------------

@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html',
                           meals_courses=mongo.db.meals_courses.find(),
                           cuisines=mongo.db.cuisines.find())


#---------Insert Recipe Functionality---------------------

@app.route('/insert_recipe', methods=['GET', 'POST'])
def insert_recipe():
    meal_course_type = request.form.get('meal_course_type')
    meal_id = mongo.db.meals_courses.find_one(
        {"meal_course_type": meal_course_type})["_id"]

    cuisine = request.form.get('cuisine')
    cuisine_id = mongo.db.cuisines.find_one({"cuisine": cuisine})["_id"]

    my_user_data = request.form.to_dict()

    if 'is_vegetarian' in my_user_data:
        my_user_data['is_vegetarian'] = True
    else:
        my_user_data['is_vegetarian'] = False
    my_user_data['is_vegetarian']
    
    if 'is_vegan' in my_user_data:
        my_user_data['is_vegan'] = True
    else:
        my_user_data['is_vegan'] = False
    my_user_data['is_vegan']

    if 'is_glutenFree' in my_user_data:
        my_user_data['is_glutenFree'] = True
    else:
        my_user_data['is_glutenFree'] = False
    my_user_data['is_glutenFree']
    
    if 'is_dairyFree' in my_user_data:
        my_user_data['is_dairyFree'] = True
    else:
        my_user_data['is_dairyFree'] = False
    my_user_data['is_dairyFree']

    recipe = {
        'add_photo': request.form.get('add_photo'),
        'recipe_name': request.form.get('recipe_name'),
        'recipe_description': request.form.get('recipe_description'),
        'meal_course_type': meal_id,
        'cuisine': cuisine_id,
        'serves': request.form.get('serves'),
        'time': request.form.get('time'),
        'is_vegetarian': my_user_data['is_vegetarian'],
        'is_vegan': my_user_data['is_vegan'],
        'is_glutenFree':  my_user_data['is_glutenFree'],
        'is_dairyFree': my_user_data['is_dairyFree'],
        'add_ingredients': request.form.get('add_ingredients'),
        'method': request.form.get('method')
    }
    recipes = mongo.db.recipes.insert_one(recipe)

    return redirect(url_for('get_recipes'))


#---------Edit Recipe Page Functionality---------------------

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    meal_name = mongo.db.meals_courses.find_one(
        {"_id": ObjectId(the_recipe.get("meal_course_type"))})["meal_course_type"]
    cuisine_name = mongo.db.cuisines.find_one(
        {"_id": ObjectId(the_recipe.get("cuisine"))})["cuisine"]

    return render_template('editrecipe.html', recipe=the_recipe,
                           meals_courses=mongo.db.meals_courses.find(),
                           cuisines=mongo.db.cuisines.find(),
                           cuisine=cuisine_name,
                           meal_course_type=meal_name)


#---------Update Recipe Functionality---------------------

@app.route('/update_recipe/<recipe_id>', methods=['GET', 'POST'])
def update_recipe(recipe_id):
    meal_course_type = request.form.get('meal_course_type')
    meal_id = mongo.db.meals_courses.find_one(
        {"meal_course_type": meal_course_type})["_id"]

    cuisine = request.form.get('cuisine')
    cuisine_id = mongo.db.cuisines.find_one({"cuisine": cuisine})["_id"]

    my_user_data = request.form.to_dict()

    if 'is_vegetarian' in my_user_data:
        my_user_data['is_vegetarian'] = True
    else:
        my_user_data['is_vegetarian'] = False
    my_user_data['is_vegetarian']
    
    if 'is_vegan' in my_user_data:
        my_user_data['is_vegan'] = True
    else:
        my_user_data['is_vegan'] = False
    my_user_data['is_vegan']

    if 'is_glutenFree' in my_user_data:
        my_user_data['is_glutenFree'] = True
    else:
        my_user_data['is_glutenFree'] = False
    my_user_data['is_glutenFree']
    
    if 'is_dairyFree' in my_user_data:
        my_user_data['is_dairyFree'] = True
    else:
        my_user_data['is_dairyFree'] = False
    my_user_data['is_dairyFree']

    recipes = mongo.db.recipes
    recipes.update({'_id': ObjectId(recipe_id)},
                   {
        'add_photo': request.form.get('add_photo'),
        'recipe_name': request.form.get('recipe_name'),
        'recipe_description': request.form.get('recipe_description'),
        'meal_course_type': meal_id,
        'cuisine': cuisine_id,
        'serves': request.form.get('serves'),
        'time': request.form.get('time'),
        'is_vegetarian': my_user_data['is_vegetarian'],
        'is_vegan': my_user_data['is_vegan'],
        'is_glutenFree': my_user_data['is_glutenFree'],
        'is_dairyFree': my_user_data['is_dairyFree'],
        'add_ingredients': request.form.get('add_ingredients'),
        'method': request.form.get('method')
    })
    return redirect(url_for('get_recipes'))


#---------Delete Recipe Functionality---------------------

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))


#---------Browse Categories Page Functionality---------------------

@app.route('/get_categories')
def get_categories():
    return render_template("categories.html",
                           meals_courses=mongo.db.meals_courses.find().sort("meal_course_type"),
                           cuisines=mongo.db.cuisines.find().sort("cuisine"))


#---------Edit Category Pages Functionality---------------------

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


#---------Update Category Functionality---------------------

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


#---------Delete Categories Functionality---------------------

@app.route('/delete_meal/<meal_id>')
def delete_meal(meal_id):
    mongo.db.meals_courses.remove({'_id': ObjectId(meal_id)})
    return redirect(url_for('get_categories'))


@app.route('/delete_cuisine/<cuis_id>')
def delete_cuisine(cuis_id):
    mongo.db.cuisines.remove({'_id': ObjectId(cuis_id)})
    return redirect(url_for('get_categories'))


#---------Add Category Page Functionality---------------------

@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')


#---------Insert Category Functionality---------------------

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


#---------END OF FUNCTION DEFINITIONS---------------------

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

#---------END OF app.py---------------------