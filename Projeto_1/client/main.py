# export FLASK_APP=main.py
# export FLASK_dev=development
# flask run

#--------------------------------------- Imports -----------------------------------------#
import os
import sys
import socket
import time
import threading
from flask import Flask, url_for, redirect, jsonify, request, render_template

#-----------------------------------------------------------------------------------------#
#----------------------------------- Variables -------------------------------------------#

data = []
date = ''
last_date = ''

server = ("127.0.0.1", 4242)

sock = None
connFlag = True

#-----------------------------------------------------------------------------------------#

#-----------------------------------------------------------------------------------------#
os.system('cls||clear')

app = Flask(__name__)

@app.route('/')
def start():
    return render_template("index.html")

@app.route('/getData', methods=['POST', 'GET'])
def getData():
    global data
    return jsonify(data)

if __name__ == "__main__":
    threading.Thread(target=lambda : app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)).start()


#-----------------------------------------------------------------------------------------#

#-----------------------------------------------------------------------------------------#
# Start client TCP/IP
def definition():
    global server, log, sock, data, connFlag
    last_time = time.time()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created...\n")
    except socket.error as err:
        print("Socket creation failed, error : " + str(err))

    print("Connecting....\n")
    
    try:    
        sock.connect(server)
        print("Connection OK...\n")    
        #connFlag = False
        while(connFlag):
            if int(time.time()-last_time) > 1:
                connexion()
                last_time = time.time()
    except socket.error as err:
        print("Socket connection failed, error: " + str(err))

def connexion():
    global sock, date, last_date, data, connFlag

    sock.send("date".encode())
    rec = None
    rec = sock.recv(1024).decode("utf-8")

    date = rec
    #print(date)

    if(date != last_date):

        for i in range(0, 60):
            message = "profiles#" + str(i)
            sock.send(message.encode())

            rec = None
            rec = sock.recv(1024).decode("utf-8")
            #print(rec)

            try:
                data[i] = rec
            except:
                data.append(rec)

        print(data)
        last_date = date

    if(connFlag == False):
        sock.send("end".encode())

        print("Closing the socket...\n")
        sock.close()
        sys.exit(1)


threading.Thread(target=lambda : definition()).start()