from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from database_setup import Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///catalogapp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

category = session.query(Category).filter_by(name='Soccer')
categories = session.query(Category).order_by('name')

item = session.query(Item).filter_by(name='Stick')
items = session.query(Item).order_by('name')

@app.route('/')
@app.route('/catalogs/')
def home():
    """
    List all of the categories, and latest ten items
    """
    all_categories = session.query(Category).order_by('name')
    latest_items = session.query(Item).order_by('id DESC')
    return render_template('home.html',
                           all_categories=all_categories,
                           latest_items=latest_items,
                           show_categories=True)


@app.route('/catalogs/<category_name>/')
@app.route('/catalogs/<category_name>/items/')
def showCategory(category_name):
    """
    List all items in the selected category
    """
    all_categories = session.query(Category).order_by('name')
    current_category = session.query(Category).filter_by(name=category_name).one()
    filtered_items = session.query(Item).filter_by(category_id=current_category.id)
    return render_template('categories/show.html',
                            category_name= category_name,
                            all_categories=all_categories,
                            filtered_items=filtered_items,
                            show_categories=True)


@app.route('/catalogs/new/', methods=['GET', 'POST'])
def newCategory():
    """
    Allow logged users to create new category
    """
    if request.method == 'POST':
        new_category_name = request.form['name'].strip().lower()
        if new_category_name:
            # if not blank, save it to the database
            new_category = Category(name=new_category_name)
            session.add(new_category)
            try:
                session.commit()
                return redirect(
                    url_for('showCategory',
                            category_name=new_category_name))
            except IntegrityError:
                # name must be unique, so re-render form with this error
                session.rollback()
                errors = {'name': "already exists, try different name"}
                # save non-unique value to show which value exists
                values = {'name': request.form['name']}
                return render_template('categories/new.html',
                                       errors=errors,
                                       values=values)
        else:
            # if it's blank, re-render form with this error
            errors = {'name': "can't be blank"}
            return render_template('categories/new.html',
                                   errors=errors)
    else:
        # Show a form to create new category
        return render_template('categories/new.html')


@app.route('/catalogs/<category_name>/edit/', methods=['GET', 'POST'])
def editCategory(category_name):
        """
        Allow logged users to edit a category
        """
        category_to_edit = session.query(Category).filter_by(name=category_name).one()
        if request.method == 'POST':
            edited_category_name = request.form['name'].strip().lower()
            if edited_category_name:
                # if not blank, update it
                category_to_edit.name = edited_category_name
                session.add(category_to_edit)
                try:
                    session.commit()
                    return redirect(
                        url_for('showCategory',
                                category_name=edited_category_name))
                except IntegrityError:
                    # name must be unique, so re-render form with this error
                    session.rollback()
                    errors = {'name': "already exists, try different name"}
                    # save non-unique value to show which value exists
                    values = {'name': request.form['name']}
                    return render_template('categories/edit.html',
                                           category=category_to_edit,
                                           errors=errors,
                                           values=values)
            else:
                # if it's blank, re-render form with errors
                errors = {'name': "can't be blank"}
                return render_template('categories/edit.html',
                                       category=category_to_edit,
                                       errors=errors)
        else:
            # Show a form to edit category
            return render_template('categories/edit.html',
                                   category=category_to_edit)


@app.route('/catalogs/<category_name>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_name):
    """
    Allow logged users to delete a category (and items in it)
    """
    category_to_delete = session.query(Category).filter_by(name=category_name).first()
    items_to_delete = session.query(Item).filter_by(category_id=category_to_delete.id)
    if request.method == 'POST':
        for item_to_delete in items_to_delete:
            session.delete(item_to_delete)
        session.delete(category_to_delete)
        try:
            session.commit()
            return redirect(url_for('home'))
        except:
            session.rollback()
            return "An unknown error occured!"
        # Delete category and related items
        # Fake it as they are deleted
    else:
        # Show a confirmation to delete
        return render_template('categories/delete.html',
                               category_name=category_name)


@app.route('/catalogs/<category_name>/items/<item_name>/')
def showItem(category_name, item_name):
   """
   Show details of selected item
   """
   item_category = session.query(Category).filter_by(name=category_name).one()
   item_to_show = session.query(Item).filter_by(name=item_name, category_id=item_category.id).one()
   return render_template('items/show.html', item=item_to_show)


@app.route('/catalogs/<category_name>/items/new/', methods=['GET', 'POST'])
def newItem(category_name):
    """
    Allow logged users to create an item
    """
    if request.method == 'POST':
        new_item_name = request.form['name'].strip().lower()
        new_item_description = request.form['description'].strip()
        if new_item_name and new_item_description:
            # if not blank, save to database
            new_item_category = session.query(Category).filter_by(name=category_name).one()
            new_item = Item(name=new_item_name,
                            description=new_item_description,
                            category=new_item_category)
            session.add(new_item)
            try:
                session.commit()
                return redirect(url_for('showItem',
                                        category_name=category_name,
                                        item_name=new_item_name))
            except IntegrityError:
                session.rollback()
                errors = {'name': "another item has same name in this category"}
                params = {'name': new_item_name,
                          'description': new_item_description}
                return render_template('items/new.html',
                                       category_name=category_name,
                                       errors = errors,
                                       params = params)
        else:
            errors = {}
            params = {'name': '', 'description': ''}
            if new_item_name:
                params['name'] = new_item_name
            else:
                errors['name'] = "can't be blank"

            if new_item_description:
                params['description'] = new_item_description
            else:
                errors['description'] = "can't be blank"

            return render_template('items/new.html',
                                   category_name=category_name,
                                   errors = errors,
                                   params = params)
    else:
        # Show a form to edit category
        return render_template('items/new.html',
                               category_name=category_name,
                               params={'name':'',
                                       'description':''})


@app.route('/catalogs/<category_name>/items/<item_name>/edit/', methods=['GET', 'POST'])
def editItem(category_name, item_name):
    """
    Allow logged users to edit an item
    """
    item_category = session.query(Category).filter_by(name=category_name).one()
    item_to_edit = session.query(Item).filter_by(name=item_name, category_id=item_category.id).one()
    if request.method == 'POST':
        edited_item_name = request.form['name'].strip().lower()
        edited_item_description = request.form['description'].strip()
        if edited_item_name and edited_item_description:
            item_to_edit.name = edited_item_name
            item_to_edit.description = edited_item_description
            session.add(item_to_edit)
            try:
                session.commit()
                return redirect(url_for('showItem',
                                        category_name=category_name,
                                        item_name=edited_item_name))
            except IntegrityError:
                session.rollback()
                errors = {'name': "another item has same name in this category"}
                params = {'name': edited_item_name,
                          'description': edited_item_description}
                return render_template('items/edit.html',
                                       category_name=category_name,
                                       item_name=item_name,
                                       errors = errors,
                                       params = params)
        else:
            errors = {}
            params = {'name': '', 'description': ''}
            if edited_item_name:
                params['name'] = edited_item_name
            else:
                errors['name'] = "can't be blank"

            if edited_item_description:
                params['description'] = edited_item_description
            else:
                errors['description'] = "can't be blank"

            return render_template('items/edit.html',
                                   category_name=category_name,
                                   item_name=item_name,
                                   errors = errors,
                                   params = params)
    else:
        # Show a form to edit category
        return render_template('items/edit.html',
                               category_name=category_name,
                               item_name=item_name,
                               params={ 'name': item_to_edit.name,
                                        'description': item_to_edit.description})

@app.route('/catalogs/<category_name>/items/<item_name>/delete/', methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    """
    Allow logged users to delete an item
    """
    item_category = session.query(Category).filter_by(name=category_name).one()
    item_to_delete = session.query(Item).filter_by(name=item_name, category_id=item_category.id).one()
    if request.method == 'POST':
        session.delete(item_to_delete)
        try:
            session.commit()
            return redirect(url_for('showCategory', category_name=category_name))
        except:
            session.rollback()
            return "An unknown error occured!"
    else:
        # Show a confirmation to delete
        return render_template('items/delete.html',
                               category_name=category_name,
                               item_name=item_name)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
