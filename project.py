# minimal Flask application to get going
#
from flask import Flask, render_template
app = Flask(__name__)

# from lesson 1 database_setup.py
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# create a db session and connect
engine = create_engine('sqlite:///restaurantmenu.db')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# decorator functions = wrappers to existing functions - say what now?
# decorators dynamically alter the functionality of a function, method or class
# without having to directly use subclasses
# the HelloWorld() function is wrapped by app.route()
# if the site is visited (using host and port defined below) with either the root or /hello
# then HelloWorld() is called
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id = None):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    if restaurant:
        items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
        return render_template('menu.html', restaurant=restaurant, items=items)
    else:
        output = ''
        output += "<html><head><title>List Menu Items</title></head><body>"
        output += "<h2>No restaurant data found for ID#{0}</h2></body>".format(restaurant_id)
        return output


# Task 1: Create route for newMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/new')
def newMenuItem(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"


# Task 2: Create route for editMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"


# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

