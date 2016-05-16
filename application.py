from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Fake Categories
category = {'name': 'Soccer', 'id': '1'}
categories = [{'name': 'Soccer', 'id': '1'},
            {'name': 'Basketball', 'id':'2'},
            {'name':'Baseball', 'id':'3'},
            {'name':'Snowboarding', 'id':'4'},
            {'name':'Frisbee', 'id':'5'},
            {'name':'Hockey', 'id':'6'}]

# Fake Items
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
@app.route('/catalogs/')
def home():
    """
    List all of the categories, and latest ten items
    """
    return render_template('home.html',
                           categories=categories,
                           latest=items,
                           show_categories=True)

@app.route('/catalogs/new/', methods=['GET', 'POST'])
def newCategory():
    """
    Allow logged users to create new category
    """
    if request.method == 'POST':
        new_category = category
        # Save category
        # Fake it as saved
        return redirect(url_for('showCategory', category_name=request.form['name']))
    else:
        # Show a form to create new category
        return render_template('categories/new.html',
                               show_categories=False)

@app.route('/catalogs/<category_name>/edit/', methods=['GET', 'POST'])
def editCategory(category_name):
        """
        Allow logged users to edit a category
        """
        category_to_edit = category
        if request.method == 'POST':
            # Update category
            # Fake it as updated
            return redirect(url_for('showCategory', category_name=request.form['name']))
        else:
            # Show a form to edit category
            return render_template('categories/edit.html',
                                   category=category_to_edit,
                                   show_categories=False)

@app.route('/catalogs/<category_name>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_name):
    """
    Allow logged users to delete a category (and items in it)
    """
    category_to_delete = category
    items_to_delete = items
    if request.method == 'POST':
        # Delete category and related items
        # Fake it as they are deleted
        return redirect(url_for('home'))
    else:
        # Show a confirmation to delete
        return render_template('categories/delete.html',
                               category_name=category_name,
                               show_categories=False)

@app.route('/catalogs/<category_name>/')
@app.route('/catalogs/<category_name>/items/')
def showCategory(category_name):
    """
    List all items in the selected category
    """
    return render_template('categories/show.html',
                            category_name= category_name,
                            categories=categories,
                            items=items,
                            show_categories=True)

@app.route('/catalogs/<category_name>/items/new/', methods=['GET', 'POST'])
def newItem(category_name):
    """
    Allow logged users to create an item
    """
    if request.method == 'POST':
        # Create category
        # Fake it as saved
        return redirect(url_for('showItem', category_name=category_name, item_name=request.form['name']))
    else:
        # Show a form to edit category
        return render_template('items/new.html',
                               category_name=category_name,
                               params={'name':'', 'description':'', 'price':''},
                               show_categories=False)

@app.route('/catalogs/<category_name>/items/<item_name>/')
def showItem(category_name, item_name):
    """
    Show details of selected item
    """
    item_to_show = item
    return render_template('items/show.html', item=item_to_show)

@app.route('/catalogs/<category_name>/items/<item_name>/edit/', methods=['GET', 'POST'])
def editItem(category_name, item_name):
    """
    Allow logged users to edit an item
    """
    item_to_edit = item
    if request.method == 'POST':
        # Update item
        # Fake it as updated
        return redirect(url_for('showItem', category_name=category_name, item_name=request.form['name']))
    else:
        # Show a form to edit category
        return render_template('items/edit.html',
                               item=item_to_edit,
                               show_categories=False)

@app.route('/catalogs/<category_name>/items/<item_name>/delete/', methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    """
    Allow logged users to delete an item
    """
    item_to_delete = item
    if request.method == 'POST':
        # Delete category and related items
        # Fake it as they are deleted
        return redirect(url_for('showCategory', category_name=category_name))
    else:
        # Show a confirmation to delete
        return render_template('items/delete.html',
                               item=item_to_delete,
                               show_categories=False)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
