from flask import Flask
from flask import render_template
#import JSON
import socket
import sys
import os
import thread

server_address = "/var/run/power_data.sock"
app = Flask(__name__)

global power_data

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
    def listen_for_data():
	with app.test_request_context():
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
    	    	        rf_data_size = 4;
    	    	        buff = connection.recv(rf_data_size)
    	    	        (power, angle) = struct.unpack("!HH",buff)
    	    		power_data.append((power, angle))    
    	        finally:
    	    	    # Clean up the connection
    	    	    connection.close()
    thread.start_new_thread(listen_for_data,())
    print("Starting rotation and AUT measurement")
    return "Thanks for checking in!"

@app.route("/angle")
def setrotation():
    #Send command over socket to Sean's Code
    print("Set new rotation to: ")
    
@app.route("/scratch")
def scratch():
    return render_template('scratch.html')

#@app.route("/getdata")
#def serialize_plot_data():
#    data = {
#        type = "scatterpolar",
#        mode = "lines+markers",
#        r   = [],
#        theta = []
#    }
#    return JSON.serialize(data)
# This is a updata test
