from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import os, random, time,json

from mqtthandler import on_connect, on_message
from variable_container import MAX_VAL, MIN_VAL, PRINT_VALUES, DEVICE_NAME, INTERVAL

load_dotenv()

###############

def generate_value():
    return random.randrange(MIN_VAL, MAX_VAL)

def share_value(val):
    client.publish('ns/arduino_send', json.dumps
    ({
        'cmd':'value_share',
        'device_name': DEVICE_NAME,
        'val': str(val)
    }), 0)

###############

print("Fake node program started running...")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
client.username_pw_set(os.getenv('MQTT_USER'), os.getenv('MQTT_PASS'))
client.connect(os.getenv('MQTT_URL'), int(os.getenv('MQTT_PORT')))
# client.loop_forever()
client.loop_start()

print("Setup complete. Started sending values...")


while (True):
    val = generate_value()
    share_value(val)
    
    if PRINT_VALUES:
        print("[value share] " + str(val))
    
    time.sleep(INTERVAL)





