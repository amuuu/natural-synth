import json, time
import paho.mqtt.client as mqtt

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

~~~~~~~~~~~~~~~~~~~~~~~~
topic ns/raspberry_change:
~~~~~~~~~~~~~~~~~~~~~~~~
6) change_sensor_minmax [1/2 done]
{
"cmd": "change_sensor_minmax",
"min": "12",
"max": "54"
}

7) change_scale (note and type) [1/2 done]
{
"cmd": "change_scale",
"scale_name": "c#",
"scale_type": "minor"
}

8) change_octave_range [1/2 done]
{
"cmd":"change_octave_range",
"start_octave":"2",
"octave_nums":"3"
}

9) change_chord_mode_active 
{
"cmd":"change_chord_mode_active",
"isactive":"true"
}

10) change_sound_out_active [1/2 done]
{
"cmd":"change_sound_out_active",
"isactive":"true"
}

11) change_midi_out_active
{
"cmd":"change_midi_out_active",
"isactive":"true"
}

12) change_sound_wavetype [1/2 done]
{
"cmd":"change_sound_wavetype",
"wave_type":"sine"
}

13) change_sound_duration [1/2 done]
{
"cmd":"change_sound_duration",
"duration":"0.5"
}

14) introduction_request
{
"cmd": "introduction_request"
}

"""

topic = ['ns/arduino_send',
         'ns/arduino_change',
         'ns/raspberry_change']

names = []
divs = []
raspberry_info_dict={}
is_raspberry_introduced_for_first_time = False


"""
COMMANDS FOR PERIPHERAL NODES
"""

def peripheral_node_name_update(device_name, new_name):
    client_object.publish(topic[1], json.dumps({'cmd':'change_name', 'device_name': device_name, 'new_name': new_name}), 0)

def peripheral_node_activeself_update(device_name, activeself):
    client_object.publish(topic[1], json.dumps({'cmd':'change_active_self','device_name': device_name, 'activeself': activeself}), 0)

def peripheral_introduction_request():
    client_object.publish(topic[1], json.dumps({'cmd':'introduction_request'}), 0)

"""
COMMANDS FOR PROCESSING NODE
"""
def processing_node_change_sensor_minmax(min, max):
    client_object.publish(topic[2], json.dumps({'cmd':'change_sensor_minmax', 'min': min, 'max': max}), 0)

def processing_node_change_scale(scale_name, scale_type):
    client_object.publish(topic[2], json.dumps({'cmd':'change_scale', 'scale_name': scale_name, 'scale_type': scale_type}), 0)

def processing_node_change_octave_range(start_octave, octave_nums):
    client_object.publish(topic[2], json.dumps({'cmd':'change_octave_range', 'start_octave': start_octave, 'octave_nums': octave_nums}), 0)

def processing_node_change_sound_out_active(isactive):
    client_object.publish(topic[2], json.dumps({'cmd':'change_sound_out_active', 'isactive': isactive}), 0)

def processing_node_change_midi_out_active(isactive):
    client_object.publish(topic[2], json.dumps({'cmd':'change_midi_out_active', 'isactive': isactive}), 0)

def processing_node_change_sound_wavetype(wave_type):
    client_object.publish(topic[2], json.dumps({'cmd':'change_sound_wavetype', 'wave_type': wave_type}), 0)

def processing_node_change_sound_duration(duration):
    client_object.publish(topic[2], json.dumps({'cmd':'change_sound_duration', 'duration': duration}), 0)

def processing_node_introduction_request():
    client_object.publish(topic[2], json.dumps({'cmd':'introduction_request'}), 0)


"""
MQTT CALLBACKS
"""
def on_connect(client, userdata, flags, rc):
    global client_object
    global is_raspberry_introduced

    client_object = client

    count_topics=0
    for i in topic:
        client.subscribe(i)
        count_topics += 1
    
    print("Subscribed to " + str(count_topics) + " topics successfully...")
    
    peripheral_introduction_request()
    print ("Asked peripheral nodes to introduce...")

    processing_node_introduction_request()
    print ("Asked raspberry to introduce...")




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

    if msg.topic == topic[2]:
        
        cmd = data.get('cmd')

        if cmd == "raspberry_introduction":
            global is_raspberry_introduced_for_first_time
            if not is_raspberry_introduced_for_first_time:
                is_raspberry_introduced_for_first_time = True
            
            raspberry_info_dict['max_sensor_val'] = data.get('max_sensor_val')
            raspberry_info_dict['min_sensor_val'] = data.get('min_sensor_val')
            raspberry_info_dict['scale_type'] = data.get('scale_type')
            raspberry_info_dict['scale_base_note'] = data.get('scale_base_note')
            raspberry_info_dict['octave_start'] = data.get('octave_start')
            raspberry_info_dict['octave_nums'] = data.get('octave_nums')
            is_sound_out_active = data.get('is_sound_out_active')
            if is_sound_out_active == "true":
                raspberry_info_dict['is_sound_out_active'] = True
            else:
                raspberry_info_dict['is_sound_out_active'] = False
            is_midi_out_active = data.get('is_midi_out_active')
            if is_midi_out_active == "true":
                raspberry_info_dict['is_midi_out_active'] = True
            else:
                raspberry_info_dict['is_midi_out_active'] = False
            raspberry_info_dict['sound_wave_type'] = data.get('sound_wave_type')
            raspberry_info_dict['sound_duration'] = data.get('sound_duration')

            print("Recieved raspberry info...")
            print(raspberry_info_dict)

