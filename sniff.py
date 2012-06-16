# -*- coding: utf-8 -*-

import flask, os
from flask.ext.sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for

# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'



# create our little application :)
app = flask.Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/database.db'
db = SQLAlchemy(app)




class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '{A record for a person, name: %r}' % self.name




class Encounter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(80), unique=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    person = db.relationship('Person',backref=db.backref('encounters', lazy='dynamic'))

    def __init__(self, subject, person):
        self.subject = subject
        self.person = person

    def __repr__(self):
        return '{Yoyo %r}' % self.username




@app.route('/')
def browse():
    return flask.render_template('index.html',people=Person.query.all(),encounters=Encounter.query.all())


@app.route('/participants')
def participants():
    return flask.render_template('users.html',people=Person.query.all())


@app.route('/updates')
def updates():
    return flask.render_template('log.html',people=Person.query.all())

@app.route('/encounters')
def encounters():
    return flask.render_template('encounters.html',people=Person.query.all(),encounters=Encounter.query.all())

@app.route('/hello')
def hello():
    return 'Hello Dima'

@app.route('/hellodb')
def hello():
    db.create_all()
    return 'Hello DB'



@app.route('/add_a_person',methods=['POST'])
def add_person():
    new_person=Person(request.form.get('name', 'Not in the request'))
    db.session.add(new_person)
    db.session.commit()
    return redirect(url_for('participants'))

@app.route('/add_an_encounter',methods=['POST'])
def add_encounter():
    new_encounter=Encounter(request.form.get('subject', 'Not in the request'),Person.query.filter_by(id=int(request.form['person'])).first())
    db.session.add(new_encounter)
    db.session.commit()
    return redirect(url_for('encounters'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
