from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import date
Base = declarative_base()
class User(Base):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    join_date = Column(Date, default=date.today)

    archives = relationship("Archive", back_populates="user")
    ratings = relationship("Rating", back_populates="user")

class Movie(Base):
    __tablename__ = 'Movies'
    movie_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    director = Column(String(100))
    release_year = Column(Integer)
    tmdb_id = Column(Integer, unique=True)
    external_rating = Column(DECIMAL(3,1))
    last_updated = Column(Date)

    archives = relationship("Archive", back_populates="movie")
    ratings = relationship("Rating", back_populates="movie")

class Archive(Base):
    __tablename__ = 'Archive'
    archive_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    movie_id = Column(Integer, ForeignKey('Movies.movie_id'))
    date_added = Column(Date, default=date.today)
    watching_status = Column(String(50))

    user = relationship("User", back_populates="archives")
    movie = relationship("Movie", back_populates="archives")

class Rating(Base):
    __tablename__ = 'Ratings'
    rating_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    movie_id = Column(Integer, ForeignKey('Movies.movie_id'))
    score = Column(Integer)
    comment = Column(Text)

    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")

