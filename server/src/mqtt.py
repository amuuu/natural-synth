import json
import paho.mqtt.client as mqtt


"""
topic sensor_data:
{
"device_name/ip": sth,
"sensor_type": sth,
"value": sth
}

topic info:
{
"device_name/ip": sth,
"is_active": sth
}

"""

topic = ['ns/arduino_send',
         'ns/arduino_change']


def on_connect(client, userdata, flags, rc):
    for i in topic:
        # client.subscribe(i)
        pass


def on_message(client, userdata, msg):
    # with app.app_context():
    #     if msg.topic == topic[0]:
    #         data = json.loads(msg.payload.decode()) #data.get('product_id')
    #         # update the respective div's content area in the page

    
    
    #     # we probably don't even need this because server always sends out this message and others only recieve.
    #     # if msg.topic == topic[1]:
    #     #     data = json.loads(msg.payload.decode())
    pass            

# changing the name of a node and inform that node.
def peripheral_node_name_update(new_name):
    # client.publish(topic[1], json.dumps({'temperature': instance.default_temperature}), 0)
    pass


# changing the status of a node. after a node recieves the command to deactivate, it stops sending data until it recieves activation again                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
def peripheral_node_activeself_update(target_ip): # ip or name
    pass


