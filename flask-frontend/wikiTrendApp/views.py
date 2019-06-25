from wikiTrendApp import app
from flask import request, jsonify, render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", query="")

@app.route('/result')
def search():
    return render_template("result.html")
