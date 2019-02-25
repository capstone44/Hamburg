import socket
import sys
import os

server_address = "/var/run/power_data.sock"
# Make sure the socket does not already exist
try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(server_address)
while True:
  server.listen(1)
  conn, addr = server.accept()
   try:
        # Receive the data in small chunks and retransmit it
        while True:
            #RF Data Size
            rf_data_size = 32;
            buff = connection.recv(rf_data_size)
            (power, angle) = struct.unpack("!HH",buff)
            #Push power and angle off onto a global structure (Redis? Another KV store? a crazy global variable???)
            
    finally:
        # Clean up the connection
        connection.close()