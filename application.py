from flask import Flask

app = Flask(__name__)

@app.route('/')
@app.route('/catalogs/')
def Catalogs():
    return """This is home page of the application. This page will be for
              listing categories and items in it."""

@app.route('/catalogs/new', methods=['GET', 'POST'])
def NewCatalog():
    return "This page will be for creating a new category"

@app.route('/catalogs/<catalog_name>/')
@app.route('/catalogs/<catalog_name>/items')
def ShowCatalog(catalog_name):
    return "This page will be for listing items in catalog %s" % catalog_name

@app.route('/catalogs/<catalog_name>/edit', methods=['GET', 'POST'])
def EditCatalog(catalog_name):
    return "This page will be for editing catalog %s" % catalog_name

@app.route('/catalogs/<catalog_name>/delete', methods=['GET', 'POST'])
def DeleteCatalog(catalog_name):
    return "This page will be for deleting catalog %s, and items in it " % catalog_name

@app.route('/catalogs/`<catalog_name>`/items/new', methods=['GET', 'POST'])
def NewItem(catalog_name):
    return "This page will be for creating new item in catalog %s." % catalog_name

@app.route('/catalogs/<catalog_name>/items/<item_name>')
def ShowItem(catalog_name, item_name):
    return "This page will show item %s, from catalog %s." % (item_name, catalog_name)

@app.route('/catalogs/<catalog_name>/items/<item_name>/edit', methods=['GET', 'POST'])
def EditItem(catalog_name, item_name):
    return "This page will be for editing item %s, from catalog %s." % (item_name, catalog_name)

@app.route('/catalogs/<catalog_name>/items/<item_name>/delete', methods=['GET', 'POST'])
def DeleteItem(catalog_name, item_name):
    return "This page will be for deleting item %s, from catalog %s." % (item_name, catalog_name)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
