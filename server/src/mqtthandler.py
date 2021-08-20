import json
import paho.mqtt.client as mqtt

# IMPORTANT IMPORTANT 
# in the beginning each node should subscribe to topics
# then it should introduce itself
# then start sending data
# After each node recieves changes information (whether it being active self or name change), it must send a node_introduction command to the network
# then start sendign data again

"""
JSON FORMAT:

~~~~~~~~~~~~~~~~~~~~~~~~
topic ns/arduino_send:
~~~~~~~~~~~~~~~~~~~~~~~~
1) value_share command:
    {
    "cmd":"value_share",
    "device_name": "sth",
    "val": 12341.23
    }

2) node_introduction command:
    {
    "cmd":"node_introduction",
    "device_name": sth,
    "sensor_type": sth,
    "is_active": true
    "old_name": "-"
    }

~~~~~~~~~~~~~~~~~~~~~~~~
topic ns/arduino_change:
~~~~~~~~~~~~~~~~~~~~~~~~
3) change_active_self command:
    {
    "cmd": "change_active_self",
    "device_name": "sth",
    "activeself": "sth"
    }

4) change_name command:
    {
    "cmd": "change_name",
    "device_name": "device",
    "new_name": "new_name"
    }

5) introduction_request command:
    {
    "cmd": "introduction_request"
    }
"""

topic = ['ns/arduino_send',
         'ns/arduino_change']

names = []
divs = []

# changing the name of a node and inform that node.
def peripheral_node_name_update(device_name, new_name):
    client_object.publish(topic[1], json.dumps({'cmd':'change_name', 'device_name': device_name, 'new_name': new_name}), 0)


# changing the status of a node. after a node recieves the command to deactivate, it stops sending data until it recieves activation again                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
def peripheral_node_activeself_update(device_name, activeself): # ip or name
    client_object.publish(topic[1], json.dumps({'cmd':'change_active_self','device_name': device_name, 'activeself': activeself}), 0)

def introduction_request():
    client_object.publish(topic[1], json.dumps({'cmd':'introduction_request'}), 0)

def on_connect(client, userdata, flags, rc):
    global client_object
    client_object = client

    count_topics=0
    for i in topic:
        client.subscribe(i)
        count_topics += 1
    print("Subscribed to " + str(count_topics) + " topics successfully...")

def on_message(client, userdata, msg):
    # try:
    data = json.loads(msg.payload.decode())

    if msg.topic == topic[0]:
    
        cmd = data.get('cmd')
        name = data.get('device_name')
        
        if cmd == "node_introduction":

            sensor_type = data.get('sensor_type')
            is_active = data.get('is_active')
            if is_active=="true":
                is_active_bool = True
            elif is_active == "false":
                is_active_bool = False
            
            # there is a new name we haven't seen before. it's either a new device or a device we know but with a new name
            if name not in names:
                
                old_name = data.get('old_name')
                
                if old_name == "-":
                    print("Node \"" + name + "\" didn't exist before. Added to list now.")
                    names.append(name)
                    divs.append({"name": name, "sensor_type": sensor_type, "is_active": is_active_bool})

                else:
                    for div in divs:
                        if div['name'] == old_name:
                            div['name'] = name

            
            ## the name is known. And hasn't changed. So the only reason that this cmd must've been sent is the fact that active self has changed
            else:
                for div in divs:
                    if div['name'] == name and div['is_active'] != is_active_bool:
                        div['is_active'] = is_active_bool
                        print("Node \"" + name + "'s activity just toggled.")
                    
        
        if cmd == "value_share":
            
            val = data.get('val')

                # show in the div
                # it can be done easily with ajax but doesn't it must be with socket to work properly and seamlessly
    # except:
    #     print("Message parse error...")