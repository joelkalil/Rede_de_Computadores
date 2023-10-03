# export FLASK_APP=main.py
# export FLASK_dev=development
# flask run

#--------------------------------------- Imports -----------------------------------------#
import os
import sys
import socket
import time
import threading
import csv
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

    if request.method == 'GET':
        profile_id = request.args.get('profile', default=0)

    path = './logs/profiles#' + str(profile_id) + '.txt'
    date, data_profile = read_csv(path, profile_id)

    return jsonify({
        'x': date,
        'y': data_profile
    })

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

        #print(data)
        last_date = date
        updateFiles()

    if(connFlag == False):
        sock.send("end".encode())

        print("Closing the socket...\n")
        sock.close()
        sys.exit(1)

# Function to get the actual data and update in each log file (1 log for each profile)
def updateFiles():
    global date, data

    for i in range(0, 60):
        # New line content to add in the log
        new_log = str(date) + ',' + str(data[i]) + '\n'

        # Making the file path
        file_name = './logs/profiles#' + str(i) + '.txt'

        # Check if the file exist
        file_exist = checkIfFileExist(file_name)

        if not file_exist:
            default_text = 'Date,' + str(i) + '\n'

            with open(file_name, 'w') as file:
                file.write(default_text+new_log)
                file.close()
        else:
            with open(file_name, 'a') as file:
                file.write(new_log)
                file.close()

# Function to check if the file exist to append, or not to create.
def checkIfFileExist(file_name):
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            file.close()
            if not content:
                return False
            else:
                return True
    except FileNotFoundError:
        return False

def read_csv(file_path, index):
    date = []
    data_profile = []

    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            date.append(row['Date'])
            data_profile.append(float(row[str(index)]))

    return date, data_profile

# Thread to start connection with the server
threading.Thread(target=lambda : definition()).start()