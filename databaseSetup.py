import sys
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    @property
    def serialize(self):

        return{
            'name':self.name,
            'id':self.id,
        }

class MenuItem(Base):
    __tablename__ = 'menu_item'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(String)
    course = Column(String)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):

        return{
            'name':self.name,
            'description':self.description,
            'price':self.price,
            'course':self.course,
            'id':self.id,
        }

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.create_all(engine)
