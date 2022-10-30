# Websockets

Written by: Samuel Berton

## Goal

Since the data-processing and hardware connection are in Python, there needs to be a way to connect this program with the extension. This is achieved through websockets.

## Details

With websockets, there are two applications, a server and a client. In this case, the extension will serve as the client and the Python code will contain the server. The major difference between websockets and http is that websockets provides a bi-directional persistent connection. Where a http connection closes after it has send the message, the websocket connection stays open until either server or client close it. This makes it makes it very efficient as opposed to polling (i.e. repeatedly checking if the state has changed).

![Websockets](images/Websocket_connection.png)

When the client receives a message from the server, it can respond and vice versa, without having to request some information.

## Implementation

In BrainBrowsR, the client code is written in Javascript and the server in Python using [the websockets package](https://websockets.readthedocs.io/en/stable/). The implementation of this, is what we call BrainServR, found in [server.py](../server.py). When an instance of BrainServR is created, it first connects to the headset and then starts up the websocketsserver. When the connection between extension and server is established, the data-processing pipeline starts sending messages.

On startup the client (i.e. the extension) initializes a connection. The server, written in Python, sends the label of the SSVEP response that was detected. In Javascript a listener is added that runs a certain function depending on the message. The implementation of this can be found in [the content script](../src/content_script.js) under setUp. This function establishes the connection and creates the listener that will repond based on the message that was sent to the extension.

![Python/javascript](images/websocket-diagram.png)

## Results

There is currently a succesful connection between the extension and Python through websockets. The connection is opened and data-processing will send the action the extension has to take. This is currently working and the extension takes the action, classification has found.
