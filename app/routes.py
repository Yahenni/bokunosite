from flask import render_template, flash, redirect, url_for

from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Index Page")

@app.route('/kirill')
def kirill():
    return render_template("specialpersons/kirill.html", title="Главный пидорас")
