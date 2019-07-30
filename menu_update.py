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
Update method:
    1) find entry - use filter_by
    2) reset values
    3) add to session
    4) commit
"""

# filter_by returns a collection of objects
veggieBurgers = session.query(MenuItem).filter_by(name = 'Veggie Burger')

# find all the burgers and figure out which to update
# looks like id = 10 in this .db
for veggieBurger in veggieBurgers:
    print('-'*25)
    print(veggieBurger.id)
    print(veggieBurger.price)
    print(veggieBurger.restaurant.name)
    print('-'*25)

# make sure SQLalchemy only returns one object .one()
UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 10).one()

# check the price, s/be $5.99
print("\nid = {} price = {}".format(UrbanVeggieBurger.id, UrbanVeggieBurger.price))

# update it
UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit()

# check the update
UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 10).one()

# check the price, s/be $2.99
print("\nid = {} price = {}".format(UrbanVeggieBurger.id, UrbanVeggieBurger.price))

# let's update all veggie burgers to same price

for veggieBurger in veggieBurgers:
    if veggieBurger != '$2.99':
        veggieBurger.price = '$2.99'
        session.add(veggieBurger)
        session.commit()

