import json,random
import paho.mqtt.client as mqtt

from variable_container import INTERVAL, DEVICE_NAME

topic = ['ns/arduino_send',
         'ns/arduino_change']


def introduction_send():
    client_object.publish(topic[0], json.dumps
    ({
        'cmd':'node_introduction',
        'device_name': DEVICE_NAME,
        'sensors':
        {
            '0':
            {
                'sensor_type': 'FakeSensor1',
                'should_invert_quantize': 'false',
                'is_active': 'true',
                'sound_wave_type': 'sine',
                'sound_intensity': '1.0'
            },
            '1':
            {
                'sensor_type': 'FakeSensor2',
                'should_invert_quantize': 'false',
                'is_active': 'true',
                'sound_wave_type': 'square',
                'sound_intensity': '1.0'
            }
        },
        'is_active': 'true',
        'old_name': '-',
        'send_interval': str(INTERVAL),
        'is_test_mode_active': 'false' 
    }), 0)

# def share_value(val):
#     client_object.publish(topic[0], json.dumps
#     ({
#         'cmd':'value_share',
#         'device_name': DEVICE_NAME,
#         'val': str(val)
#     }), 0)


def on_connect(client, userdata, flags, rc):
    global client_object
    client_object = client

    count_topics=0
    for i in topic:
        client.subscribe(i)
        count_topics += 1
    
    print('[mqtt handler] Subscribed to ' + str(count_topics) + ' topics successfully...')
    
    introduction_send()
    print('[mqtt handler] Introduced fake node to server...')

def on_message(client, userdata, msg):
    cmd = ''
    data = json.loads(msg.payload.decode())
