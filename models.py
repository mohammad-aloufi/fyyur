from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate =Migrate(app, db)

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres =db.Column(db.ARRAY(db.String), nullable=True)
    upcoming_shows =db.Column(db.Integer, nullable =True)
    past_shows =db.Column(db.Integer, nullable=True)
    website =db.Column(db.String(), nullable=True)
    seeking_talent =db.Column(db.Boolean(), nullable =False, default=True)
    seeking_description =db.Column(db.String(), nullable=True)
    show = db.relationship('Show', backref='Venue', lazy=True)



class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres =db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website =db.Column(db.String(), nullable =True)
    seeking_venue =db.Column(db.Boolean(), default =False, nullable =False)
    seeking_description =db.Column(db.String(), default =False, nullable =False)
    past_shows =db.Column(db.Integer(), default=0, nullable=False)
    upcoming_shows =db.Column(db.Integer, default=0, nullable =False)
    show = db.relationship('Show', backref='artist', lazy=True)


class Show(db.Model):
    __tablename__ ='shows'
    id =db.Column(db.Integer(), primary_key=True)
    venue_id =db.Column(db.Integer(), db.ForeignKey('Venue.id'), nullable =False)
    artist_id =db.Column(db.Integer(), db.ForeignKey('Artist.id'), nullable =False)
    artist_name =db.Column(db.String(), nullable =False)
    start_time =db.Column(db.String(), nullable =False)
    artist_image =db.Column(db.String(), nullable =False)
