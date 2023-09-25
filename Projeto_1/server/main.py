# --------------------------------------------------------------------------------------------------------------------- #
# Created by : Joel Pontes                                                                                              #
# Date : 09/2023                                                                                                        #
# Version : 1.0                                                                                                         #
# --------------------------------------------------------------------------------------------------------------------- #

# --------------------------------------------------------------------------------------------------------------------- #
# Imports ------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------- #

import socket
import sys, os
import time
import random
import threading
import pandas as pd

# --------------------------------------------------------------------------------------------------------------------- #
# Define the Functions ------------------------------------------------------------------------------------------------ #
# --------------------------------------------------------------------------------------------------------------------- #

# The command to execute the script in shell is "python3 main.py"
# To this case, which aren't arguments, the address will set as default
# If you want to define an address, you can use "python3 main.py IP", example ("python3 main.py 127.0.0.1")
# If you want to define an address and port, use "python3 main.py IP Port", example ("python3 main.py 127.0.0.1 4000")

def define_server(args):
    # server = (Adress_IP, Port)
    if len(args) == 2:
        server = (args[1], 4242)
    
    elif len(args) == 3:
        server = (args[1], int(args[2]))
    
    else:
        # Adress default
        server = ('127.0.0.1', 4242)

    return server

# --------------------------------------------------------------------------------------------------------------------- #

# Thread to update time.

def clock():
    global last_time, max_time

    # Getting actual clock_index
    f = open('clock.txt', "r")
    current_index = int(f.read())

    while current_index <= max_time:
        
        if int(time.time()-last_time) > 15:
            current_index += 1
            last_time = time.time()
            #print(current_index)
            # Updating new index
            f = open('clock.txt', "w")
            f.write(str(current_index))
            f.close()

# --------------------------------------------------------------------------------------------------------------------- #

# This is the function that will be executed by the child, after the fork
# This means that each client connected to the server will execute this script
# So, we started waiting a message from client
# If the length of the message isn't at least 10, this probably is a void message from POCT
# The void message means that all messages are already sent
# If the length of the message is bigger than 10, we can suppose that is a HL7 message
# So, we will call the functions to treat and to generate a JSON of message
# In the end, we will close the connection and close the children

def handle_client(connection, client):
    
    print("Connection from %s port %s" % client)
    
    while True:
        f = open('clock.txt', "r")
        current_index = int(f.read())
        #print(current_index)
        message = connection.recv(sizeMessage).decode("utf-8")
        print("Message received from %s port %s" % client)
        print(message)

        if message == 'date':
            message = str(pv['Date'][current_index])

        elif message == 'pv_10kw':
            message = str(pv['P # [W]'][current_index])

        elif message.split('#')[0] == 'profiles':
            index = message.split('#')
            #print(index)
        
            if index[1].isdigit() and int(index[1]) in range(0,60):
                message = str(profiles[index[1]][current_index])
            else:
                message = 'error index profiles'

        elif message == 'end':
            break
        
        else:
            message = 'error message'

        connection.send(message.encode())
    
    print("Stopping connection with %s port %s" %client)

    # Closing the connection
    connection.close()
    os._exit(0)

# --------------------------------------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------------------------------- #
# Define variables ---------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------- #

# Setting random seed
random.seed(time.time())

# Getting server host and port
server = define_server(sys.argv)

# Number of clients to be connected on the server
number_of_clients = 10 

# Size of the message in TCP/IP
sizeMessage = 1024

# Data Read
pv = pd.read_csv('data/new_pv_10kw.csv')
profiles = pd.read_csv('data/new_profiles.csv.data')

# Last index of dataframe
max_time = pv['Date'].size-1

# I divided by 2 to garantee that the index will no start close to the end of the dataframe
f = open('clock.txt', "w")
f.write(str(random.randint(0, (max_time-1)/2)))
f.close()

# Last time
last_time = time.time()

# Clock Thread
threading.Thread(target=lambda : clock()).start()

# --------------------------------------------------------------------------------------------------------------------- #
# Main ---------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------------- #

# Create a TCP/IP socket
# Protocole default to create the socket
# Print the message for each cas (success or error)
# In the case of don't be succeed to create the socket, the script will close (This can be changed to try sometimes before do it)

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created...\n")

except socket.error as err:
    print("Socket creation failed, error : " + str(err) + "\n")
    exit(0)

# Bind the socket to the port
# Protocole default to bind the server
# Print the message for each cas (success or error)
# In the case of don't be succeed to do the bind, the script will close (This can be changed to try sometimes before do it)
# The bind can have problems if the port is already in use, or if the IP is wrong

try:
    sock.bind(server)
    print('Starting up on %s port %s' % server)

except socket.error as err:
    print("Socket bind failed, error : " + str(err) + "\n")
    exit(0)


# Listen for income connections
# We use the sock.listen() to do the server start to wait for client's connections
# The number_of_clients is a constant that means the number of clients that tried the connection but have not accepted
# When this happens, the client should try again

try:
    sock.listen(number_of_clients)
    print("Server waiting for connection ...")
except socket.error as err:
    print("Socket listen failed, error : " + str(err) + "\n")
    exit(0)

# Infinity loop

while True:

    # So, when a client tried the connection, and the serve accept it, we will create a fork
    # The fork means we will create a copy of the script that will be executed by the client
    # But, at the same time, the server keep running
    # Look :
    # Parent (1 client) -> Parent and child scripts running
    # Parent (2 clients) -> Parent, child_1 and child_2 scripts running
    # ....

    connection, client = sock.accept()
    child_pid = os.fork()

    # child_pid = 0 means we are in the child fork, and we need to run the client script
    # child_pid = 1 means we are in the parent, and we need to run the server script
    # child_pid = -1 means some error

    if child_pid == 0 :
        handle_client(connection, client)
            
    elif child_pid > 0 :
        # Routine to be executed after the creation of a child
        pids = (os.getpid(), child_pid)
        print("\nParent: %d, Child: %d" %pids)

    elif child_pid == -1 :
        print("Fork failed !")