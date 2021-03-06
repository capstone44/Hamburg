from flask import Flask
from flask import render_template
from flask import request
import json
import socket
import sys
import os
import threading
import struct
import math
from runsystem import *

server_address = "/tmp/power_data.sock"
app = Flask(__name__)

global power_data
power_data = []

global sysrunning
sysrunning = False

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
    global sysrunning
    if sysrunning:
        pass
    else:
        sysrunning = True
        start_test()
    print(power_data)
    return render_template('plotmeasurement.html')

@app.route("/reset")
def reset_data():
    global power_data
    power_data = []
    return "RESET OK"

@app.route("/start")
def start_test():
    #Send command to Sean to start AUT rotation and measurement...
    def listen_for_data():
        # Make sure the socket does not already exist
        try:
            os.unlink(server_address)
        except OSError:
            if os.path.exists(server_address):
                raise
        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(server_address)
        while True:
            server.listen(1)
            conn, addr = server.accept()
            try:
                # Receive the data in small chunks and retransmit it
                while True:
                    #RF Data Size
                    rf_data_size = 16;
                    buff = conn.recv(rf_data_size)
                    if buff:
                        if len(buff) == rf_data_size:
                            (power, angle) = struct.unpack("dd",buff)
                            print("Power: %f, Angle: %f" % (power, angle))
                            power_data.append((power, angle))
                        else:
                            print("I got some garbage...")
                    else:
                        break
            finally:
                # Clean up the connection
                conn.close()
    t = threading.Thread(target=listen_for_data)
    t.start()
    print("Starting rotation and AUT measurement")
    return "OK"

@app.route("/runsystem", methods=['POST'])
def exec_system():
    #Send command over socket to Sean's Code
    if not request.form:
        return "BAD FORM DATA"
    stepSize = int(request.form['stepSize'])
    rotationAng = int(request.form['rotAng'])
    print("Executing measurement with step size: "+ str(stepSize) + " and rotation of: " + str(rotationAng))
    t2 = threading.Thread(target=runsystem,args=(stepSize,rotationAng))
    t2.start()
    return "OK"

def convert_to_db(x):
    return 20 * math.log10(x)

@app.route("/getdata")
def serialize_plot_data():
    r = []
    theta = []
    for i in range(len(power_data)):
        r.append(power_data[i][0])
        theta.append(power_data[i][1])
    r = [convert_to_db(x) for x in r]
    max_val = max(r)
    r = [x - max_val for x in r]
    data = {
        "type" : "scatterpolar",
        "mode" : "lines+markers",
        "r"   : r,
        "theta" : theta
    }
    return json.dumps(data)
