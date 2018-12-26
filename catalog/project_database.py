# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 11:37:40 2018

@author: Nicolas
"""

import os 
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine 

Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    name = Column(String(250), nullable=False)
    email = Column(String(250),nullable=False)
    picture = Column(String(250))
    id = Integer(Integer, primary_key=True)

class Mineral(Base):
    __tablename__ = 'stones'
    
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        #Return object data in easily serializeable format
        return {
                'id': self.id,
                'name': self.name,
        
                }
    
    
class Item(Base):
    __tablename__ = 'properties'
    
    name = Column(String(30),nullable=False)
    origin = Column(String(80))
    id = Column(Integer, primary_key=True)
    colour = Column(String(250))
    price = Column(String(10))
    hardness = Column(String(10))
    description = Column(String(1000))
    mineral_id = Column(Integer, ForeignKey('stones.id'))
    stones = relationship(Mineral)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


    
    @property
    def serialize(self):
        #Return object data in easily serializeable format
        return {
                'name': self.name,
                'origin': self.origin,
                'colour':self.colour,
                'id': self.id,
                'price': self.price,
                'hardness':self.hardness,
                'description:':self.description,
                'mineral_id': self.mineral_id}


engine = create_engine('sqlite:///mineralsitems.db')


Base.metadata.create_all(engine)