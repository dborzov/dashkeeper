import flask, os, random, json
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
app.config['SQLALCHEMY_DATABASE_URI'] =  os.environ.get('DATABASE_URL', 'sqlite:///db/database.db')

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
    return flask.render_template('index.html')



if __name__ == '__main__':
    app.run()
    #port = int(os.environ.get('PORT', 5000)) these settings are for heroku, not working locally :(
    #app.run(host='0.0.0.0', port=port)
