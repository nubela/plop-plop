from web.app import app
from flask import render_template


@app.route('/', methods=['GET'])
def index():
    return render_template("skeleton.html")