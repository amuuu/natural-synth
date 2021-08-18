import json
import paho.mqtt.client as mqtt

"""
topic arduino_send:
{
"name/ip": sth,
"sensor_type": sth,
"is_active": true
"val": sth,
}

topic arduino_change:
{
"device_name/ip": sth,
"is_active": sth
}

"""

topic = ['ns/arduino_send',
         'ns/arduino_change',
         'ns/server_introduction']

names = []
divs = []

# changing the name of a node and inform that node.
def peripheral_node_name_update(client, device, new_name):
    client.publish(topic[1], json.dumps({'cmd':'changename', 'device': device, 'new_name': new_name}), 0)


# changing the status of a node. after a node recieves the command to deactivate, it stops sending data until it recieves activation again                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
def peripheral_node_activeself_update(client, device, activeself): # ip or name
    client.publish(topic[1], json.dumps({'cmd':'changeactiveself','device': device, 'activeself': activeself}), 0)

# server introducing herself in the beginning
def server_introduction(client):
    client.publish(topic[2], json.dumps({'name': 'server'}))


def on_connect(client, userdata, flags, rc):
    for i in topic:
        client.subscribe(i)
    server_introduction(client)
    print("Subscribed to topics successfully...")

def on_message(client, userdata, msg):
    
    if msg.topic == topic[0]:
    
        data = json.loads(msg.payload.decode()) #data.get('product_id')
    
        name = data.get('name')
        sensor_type = data.get('sensor_type')
        val = data.get('val')
        is_active = data.get('is_active')
        if is_active=="true":
            is_active = True
        elif is_active == "false":
            is_active = False
            
        if name not in names:
            print("Node \"" + name + "\" didn't exist before. Added to list now.")
            names.extend(name)
            # ADD the respective div's content area in the page
            divs.append({"name": name, "sensor_type": sensor_type, "val": val, "is_active": is_active})
        else:
            # UPDATE the respective div's content area in the page
            pass
        
    
    #     # we probably don't even need this because server always sends out this message and others only recieve.
    #     # if msg.topic == topic[1]:
    #     #     data = json.loads(msg.payload.decode())

