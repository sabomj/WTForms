from flask import Flask, request, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required

import requests
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.debug = True

@app.route('/')
def home():
    return "Hello, world!"

#create class to represent WTForm that inherits flask form
class SongClass(FlaskForm):
    name = StringField("What is the artist's name?", validators=[Required()])
    songs = IntegerField('How many songs do you want to see?', validators=[Required()])
    email = IntegerField('What is your email?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/itunes-form')
def itunes_form():
    simpleForm = SongClass()
    return render_template('itunes-form.html', form=simpleForm) # HINT : create itunes-form.html to represent the form defined in your class

@app.route('/itunes-result', methods = ['GET', 'POST'])
def itunes_result():
    form = SongClass(request.form)
    params ={}


    if request.method == 'POST' and form.validate_on_submit():
        params['term'] = form.name.data
        params['limit'] = form.songs.data
        response = requests.get('https://itunes.apple.com/search', params = params)
        response_text= json.loads(response.text)
        result_py = response_text['results']

        return render_template('itunes-form.html', result_html = result_py)
    flash('All fields are required!')
    return redirect(url_for('itunes_form')) #this redirects you to itunes_form if there are errors

if __name__ == '__main__':
    app.run()
