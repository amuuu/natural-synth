# Natural

Natural is an open-source digital IoT-based hardware synthesizer. It focuses on turning enoviormental data into sounds, but all data is transmitted remotely through the internet.

Natural works with a set of nodes that send data (Arduino nodes), the main processing node (a Raspberry Pi node), and a Flask server. Infinite number of nodes with sensors read data and send them to a central server, with the help of MQTT. The main processing unit, the synthesizer, is subscribed to the topic of which the nodes send their data to; and is constantly recieving data, and creating sounds in real time. Each Arduino node in the mesh is assigned to a track in the processing unit. The sound processing unit of the Raspberry Pi is powered by [Ava sound engine]().

A web panel is provided to the user to do these things:

- Enable/disable a node
- Change device names
- See the data each node is transmitting to the server or the data that's being transmitted to the main processing node
- [TODO] Change the natural parameters that are normally set by GPIO pins remotely. (aka control and paly with the synth remotely from the panel)

# How to build Natural for yourself?

## 1) Sensor units

For each node, these steps must be done:
1) Get the Arduino source code from the repo
2) Modify the program to match your sensor wiring
3) Upload it to your board

For the ease of use, we recommend you to use WEMOS D1 development boards. 

You can choose any set of sensors that you want; make sure that each node has proper MQTT server information and broker account settings.

## 2) Raspberry Pi

1) Install raspberian on your Raspberry Pi board.
2) Use the source code and the guide inside the [raspberry-node folder]() to write the program on your Raspberry Pi board.

Natural's main program is a combination of always doing these tasks:
- Recieving data to the server and other nodes.
- Making sound. That's why we do all of this.
- Sending USB MIDI out signal.

## 3) Server

1) Get the server from the [server folder]().
2) Follow the instructions in the folder to run it.

Once the server is up and running, you will be able to see the synth's panel from your web browser on this address: `http://127.0.0.1:5000`.

## 4) Fire up Natural!

Once you've done all the steps, just simply start running all the nodes, and the server! Then start making sounds using the enviornment. You can always add nodes with any types of sensors that you want too! Simply manage the nodes using the panel.
