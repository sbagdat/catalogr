from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


#Fake Categories
category = {'name': 'Soccer', 'id': '1'}
categories = [{'name': 'Soccer', 'id': '1'},
            {'name': 'Basketball', 'id':'2'},
            {'name':'Baseball', 'id':'3'},
            {'name':'Snowboarding', 'id':'4'},
            {'name':'Frisbee', 'id':'5'},
            {'name':'Hockey', 'id':'6'}]

#Fake Items
item =  {'name':'Stick', 'description':'Description of hockey stick', 'price':'$5.99', 'id':'1', 'category_name':'Hockey'}
items = [ {'name':'Stick', 'description':'Description of hockey stick', 'price':'$5.99', 'id':'1', 'category_name':'Hockey'},
          {'name':'Goggles', 'description':'Description of goggles', 'price':'$12.99', 'id':'2', 'category_name':'Snowboarding'},
          {'name':'Snowboard', 'description':'Description of snowboard', 'price':'$7.99', 'id':'3', 'category_name':'Snowboarding'},
          {'name':'Two Shinguards', 'description':'Description of two shinguards', 'price':'$3.99', 'id':'4', 'category_name':'Soccer'},
          {'name':'Shinguards', 'description':'Description of singuards', 'price':'$5.99', 'id':'5', 'category_name':'Soccer'},
          {'name':'Frisbee', 'description':'Description of frisbee', 'price':'$32.99', 'id':'6', 'category_name':'Frisbee'},
          {'name':'Bat', 'description':'Description of bat', 'price':'$4.99', 'id':'7', 'category_name':'Baseball'},
          {'name':'Jersey', 'description':'Description of jersey', 'price':'$8.99', 'id':'8', 'category_name':'Soccer'},
          {'name':'Soccer Cleats', 'description':'Description of soccer cleats', 'price':'$27.99', 'id':'9', 'category_name':'Soccer'}]


@app.route('/')
@app.route('/catalogs')
def Home():
    """
    List all of the categories, and latest ten items
    """
    return render_template('home.html',
                           categories=categories,
                           latest=items,
                           show_categories=True)

@app.route('/catalogs/new', methods=['GET', 'POST'])
def NewCategory():
    """
    Allow users to create new category
    """
    if request.method == 'POST':
        # Save the newly created category to the database
        category_name = request.form['name']
        # Fake it like saved to db
        return redirect(url_for('Home'))
    else:
        # Show a form to create new category
        return render_template('categories/new.html',
                               show_categories=False)

@app.route('/catalogs/<category_name>/edit', methods=['GET', 'POST'])
def EditCategory(category_name):
    return "This page will be for editing category %s" % category_name

@app.route('/catalogs/<category_name>/delete', methods=['GET', 'POST'])
def DeleteCategory(category_name):
    return "This page will be for deleting category %s, and items in it " % category_name

@app.route('/catalogs/<category_name>/')
@app.route('/catalogs/<category_name>/items')
def ShowCategoryItems(category_name):
    """
    List all items in the selected category
    """
    return render_template('categories/show.html',
    category_name= category_name,
    categories=categories,
    items=items,
    show_categories=True)

@app.route('/catalogs/`<category_name>`/items/new', methods=['GET', 'POST'])
def NewItem(category_name):
    return "This page will be for creating new item in category %s." % category_name

@app.route('/catalogs/<category_name>/items/<item_name>')
def ShowItem(category_name, item_name):
    return "This page will show item %s, from category %s." % (item_name, category_name)

@app.route('/catalogs/<category_name>/items/<item_name>/edit', methods=['GET', 'POST'])
def EditItem(category_name, item_name):
    return "This page will be for editing item %s, from category %s." % (item_name, category_name)

@app.route('/catalogs/<category_name>/items/<item_name>/delete', methods=['GET', 'POST'])
def DeleteItem(category_name, item_name):
    return "This page will be for deleting item %s, from category %s." % (item_name, category_name)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
