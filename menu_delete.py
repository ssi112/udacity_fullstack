"""
menu_delete

    Before we perform any operations, we must first import the necessary
    libraries, connect to our restaurantMenu.db, and create a session to
    interface with the database:

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

"""
Delete method:
    1) find entry - use filter_by
    2) session.delete(entry)
    4) commit
"""

# assuming only one entry in db
spinach = session.query(MenuItem).filter_by(name = "Spinach Ice Cream").one()
print("\nRestaurant Name: {} Menu Item ID: {}".format(spinach.restaurant.name, spinach.id))
session.delete(spinach)
session.commit()

# will return an error since it no longer exist
spinach = session.query(MenuItem).filter_by(name = "Spinach Ice Cream").one()
