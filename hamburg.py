from flask import Flask
from flask import render_template
import JSON
app = Flask(__name__)

@app.route('/static/<path:path>')
def send_js(path):
        return send_from_directory('static', path)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/quickstart")
def quickstart():
    return render_template('quickstart.html')

@app.route("/plotmeasurement")
def plotmeasurement():
    return render_template('plotmeasurement.html')

@app.route("/start")
def start_test():
    #Send command to Sean to start AUT rotation and measurement...
    print("Starting rotation and AUT measurement")

@app.route("/angle")
def setrotation():
    #Send command over socket to Sean's Code
    print("Set new rotation to: ")
    
@app.route("/scratch")
def scratch():
    return render_template('scratch.html')

@app.route("/getdata")
def serialize_plot_data():
    data = {
        type = "scatterpolar",
        mode = "markers",
        r   = [],
        theta = []
    }
    return JSON.serialize(data)
