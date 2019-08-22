# database_setup.py
import sys

# configuration code
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


# inherit features from sqlalchemy classes that correspond to tables in DB
Base = declarative_base()


# OOP representation of tables in DB
class Restaurant(Base):
    """
    Restaurant table column definitions
    """
    # special variable for sqlalchemy to associate with table
    __tablename__ = 'restaurant'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

class MenuItem(Base):
    """
    MenuItem table column definitions
    """
    __tablename__ = 'menu_item'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    # decorator method for API - defines what data to send
    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
            'restaurant_id': self.restaurant_id
        }

#############################
### insert at end of file ###
#############################

# Create an engine that stores data in the local directory's db file
engine = create_engine('sqlite:///restaurantmenu.db')

# Create all tables in the engine. This is equivalent to "Create Table" statements in SQL
Base.metadata.create_all(engine)

