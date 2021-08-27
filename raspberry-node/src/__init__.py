from flask import Flask
from dotenv import load_dotenv

import paho.mqtt.client as mqtt
import os

from .mqtthandler import on_connect, on_message

load_dotenv()

import soundhandler, soundout_thread

sound_out_thread = soundout_thread.SoundOutThread()


def create_app():
    print("Here bro")

    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
    client.username_pw_set(os.getenv('MQTT_USER'), os.getenv('MQTT_PASS'))
    client.connect(os.getenv('MQTT_URL'), int(os.getenv('MQTT_PORT')))
    # client.loop_forever()
    client.loop_start()
    

    soundhandler.init()
    soundout_thread.start()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    

    return app