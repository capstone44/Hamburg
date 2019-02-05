from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/static/<path:path>')
def send_js(path):
        return send_from_directory('static', path)

@app.route("/")
def index():
    return render_template('templates/index.html')
