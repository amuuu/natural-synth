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

## 0) Broker Service

In order for the differnt parts of the device to get connected, you need to make an account in a MQTT broker service and create user accounts for each member of the network. Bascially each node needs these information:

- Broker server address
- Broker server port
- Username (in broker service)
- Password (in broker service)
- Is SSL active or not

Additionally, pripheral nodes also need WIFI SSID and password to get connected to the internet.

## 1) Sensor units

For each node, these steps must be done:
1) Get the Arduino source code from the repo
2) Modify the program to match your sensor wiring (which is one line of code at the top, that states the PIN in which the sensor is physically connected to.)
3) Upload it to your board

For the ease of use, we recommend you to use WEMOS D1 development boards. 

You can choose any set of sensors that you want; make sure that each node has proper MQTT server information and broker account settings.

## 2) Raspberry Pi

1) Install raspberian on your Raspberry Pi board.
2) Use the source code and the guide inside the [raspberry-node folder]() to write the program on your Raspberry Pi board.

Natural's main program is a combination of always doing these tasks:

- It's constantly recieving data from sensor units and also the server. 
- It analyzes the data, and makes qunatized notes in the set scale
- Sends out sound waves and MIDI out signals

While doing all of these, if the user decides to change a setting in the dashboard, like the scale, raspberry recieves a settings change command from the server and quickly applies the new setting.

## 3) Server

1) Get the server from the [server folder]().
2) Follow the instructions in the folder to run it.

Once the server is up and running, you will be able to see the synth's panel from your web browser on this address: `http://127.0.0.1:5000`.

## 4) Fire up Natural!

Once you've done all the steps, just simply start running all the nodes, and the server! Then start making sounds using the enviornment. You can always add nodes with any types of sensors that you want too! Simply manage the nodes using the panel.
