from flask import render_template
from source.site import app

@app.route('/')
def index():
    return render_template('index.html')