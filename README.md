# Natural

Natural is an open-source digital IoT-based hardware synthesizer. It focuses on turning enoviormental data into sounds, but all data is transmitted remotely through the internet.

Natural works with a set of nodes that send data (Arduino nodes), the main processing node (a Raspberry Pi node), and a Flask server. Infinite number of nodes with sensors read data and send them to a central server, with the help of MQTT. The main processing unit, the synthesizer, is subscribed to the topic of which the nodes send their data to; and is constantly recieving data, and creating sounds in real time. Meanwhile, the user/artist can easily manipulate parameters through the Raspberry Pi's GPIO pins and change the synth's parameters. Each Arduino node in the mesh is assigned to a track in the processing unit.  The sound processing unit of the Raspberry Pi is powered by [Ava sound engine]().

A web panel is provided to the artist to manage the synth and mesh network remotely through a browser. The panel enables you to do these things:

- Enable/disable a node
- See node information such as IP
- Change node configuration such as the name
- See the data each node is transmitting to the server or the data that's being transmitted to the main processing node (in real-time)
- Change the natural parameters that are normally set by GPIO pins remotely. (aka control and paly with the synth remotely from the panel)

# How to build Natural for yourself?

## 1) Sensor units
For the ease of use, we recommend you to use WEMOS D1 development boards. 

For each node, these steps must be done:
1) Choose the proper source code for your development board (from [this repo (natural-peripheral-node)]())
2) Modify the program to match your sensor wiring
3) Write the program to your development board

You can choose any set of sensors that you want; the only point that must be considered is that each node should be aware of the server's IP and follow MQTT protocols. Implementations for programming Natural in differnet types of development boards are provided in our [natural-peripheral-node repository]().


## 2) Raspberry Pi

1) Install raspberian on your Raspberry Pi board.
2) choose your GPIO peripherals for Raspberry Pi or use the default plan provided in [this repository (natural-raspberry)]().
2) Use the source code and the guide inside [natural-raspberry]() to write the program on your Raspberry Pi board.

Natural's main program is a combination of always doing these tasks:
- Recieving from and sending data to the server topic.
- Raspberry Pi GPIO interactions (buttons/potentiometers/etc).
- Processing sound in real-time based on the parameters set on the previous two items.

## 3) Server

Clone the provided flask server in [this repository (natural-server)]() and use the provided guides to deploy your server or use it on your computer locally. **Note** that all the nodes must be aware of server's IP/domain.

Once the server is up and running, you will be able to see the synth's panel from your web browser on this address: `sth.com/sth`.

**Note** that you can't *delete* a node from Natural mesh network, but you can disable it. When you disable a node, a message will be sent to that node (with the help of MQTT) and the node will stop reading and sending data until it gets enabled again. Similarly, once you change a node's name from the panel, the new name will be sent to the node and the new value will be set as the hardware's name.

## Fire up Natural!

Once you've done all the steps, just simply start running all the nodes, and the server! Then start making sounds using the enviornment. You can always add nodes with any types of sensors that you want too! Simply manage the nodes using the panel, and the synth parameters using your Raspberry GPIO stuff!
