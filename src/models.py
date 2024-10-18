import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

#nullable
#unique (único)
#primary_key (valor irrepetible)
#default (Valor defecto)
#backref (dirección birideccional automáticamente)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), unique=True, nullable=False)
    first_name = Column(String(250))
    last_name = Column(String(250))
    email = Column(String(250), unique=True, nullable=False)
    #Conexiones
    posts = relationship('Post', back_populates='user')
    comments =  relationship('Comment', back_populates='author')
    followers = relationship('Follower', foreign_keys='Follower.user_from_id', backref='followers')
    followings = relationship('Follower', foreign_keys='Follower.user_to_id', backref='followings')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    #Conexiones
    user = relationship('User', back_populates='posts')
    media = relationship('Media', back_populates='post')
    comments = relationship('Comment', back_populates='post')

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250), unique=True, nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    #Conexiones
    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates = 'comments')
    pass

class Media (Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    type = Column(Enum('video','imagen'), nullable=False)
    url=Column(String(250))
    post_id = Column(Integer, ForeignKey('post.id'))
    #Conexiones
    post = relationship('Post', back_populates='media')
    pass

class Follower (Base):
    __tablename__ = 'follower'
    user_from_id = Column(Integer, ForeignKey('user.id'),primary_key=True)
    user_to_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    #Conexiones


## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
