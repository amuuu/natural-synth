# Natural

Natural is an open-source digital IoT-based hardware synthesizer. It focuses on turning enoviormental data into sounds, but all data is transmitted remotely through the internet.

Natural works with a set of nodes that send data (Arduino nodes), the main processing node (a Raspberry Pi node), and a UI dashboard for the user (Flask server). Infinite number of nodes with sensors read data and send them to a central server, with the help of MQTT. The main processing unit, the synthesizer, is subscribed to the topic of which the nodes send their data to; and is constantly recieving data, turning theme into musical notes, and creating two types of outputs: sound wave, and MIDI out signal.

The dashboard is provided to the user to do these things:

- Enable/disable nodes
- Change device names
- Change music theory related parameters such as scale
- Control output types
- Tune sensor data range (that helps in the conversion to musical notes)
- Change type of sound wave

# How to build Natural for yourself?

To build: Look at the [building guide](../../wiki/Building-Guide) in wiki.

To Run: Look at the [running guide](../../wiki/Running-Guide) in wiki.
