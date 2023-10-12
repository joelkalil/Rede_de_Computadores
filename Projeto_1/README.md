# Project 1 - Computer Network Discipline

## Objective

The objective of the project was to build an interface to plot graphs of generation/consumption of a house with a solar grid. So the server will start from a random point in the database, and send to the client, when it asks, the actual consumption of each cell, and after a determinate 'dt' the server increments the time variable, to simulate a real lecture.

# Installation

## 1. Client - Flask

The Flask instance is for the client. So to use it, you need to install the requirements.txt, in the project folder. To do it, you can open the folder in the shell, and use the command (I suppose that you already have python installed):

```bash
> pip install -r requirements.txt
```

Then, to start the client, you need to open the dossier "client" and start flask, you can use the commands:

```bash
> cd ./client
```

```bash
> set FLASK_APP=main
> flask run
```

## 2. Server - Python

To start the server is way more simple than the client, you need to open the server dossier, then execute the main script, you can use the commands:

```bash
> cd ./server
```

IP and PORT are optional.

```bash
> python main.py [IP] [PORT]
```
