import json,random
import paho.mqtt.client as mqtt

from . import variable_container
from .musictheoryhandler import update_settings
from .inputanalyzer import anaylze_add_add_to_buffers, update_input_settings
from .util import print_cmd_status_2, print_cmd_status_1

topic = ['ns/arduino_send',
         'ns/raspberry_change']


def introduction_response_send():
    client_object.publish(topic[1], json.dumps
    ({
        'cmd':'raspberry_introduction', 
        'max_sensor_val': str(variable_container.max_sensor_val), 
        'min_sensor_val': str(variable_container.min_sensor_val),
        'scale_type': variable_container.scale_type,
        'scale_base_note': variable_container.scale_base_note,
        'octave_start': str(variable_container.octave_start),
        'octave_nums': str(variable_container.octave_nums),
        'is_sound_out_active': str(variable_container.is_sound_out_active).lower(),
        'is_midi_out_active': str(variable_container.is_midi_out_active).lower(),
        'sound_wave_type': variable_container.sound_wave_type,
        'sound_duration': str(variable_container.sound_duration)
    }), 0)



def on_connect(client, userdata, flags, rc):
    global client_object
    client_object = client

    count_topics=0
    for i in topic:
        client.subscribe(i)
        count_topics += 1
    
    print("[mqtt handler] Subscribed to " + str(count_topics) + " topics successfully...")
    
    introduction_response_send()
    print("[mqtt handler] Introduced raspberry to server...")

def on_message(client, userdata, msg):
    cmd = ''
    data = json.loads(msg.payload.decode())

    if msg.topic == topic[0]:
    
        cmd = data.get('cmd')
        name = data.get('device_name')    
        
        if cmd == "value_share":
            val = data.get('val')

            try:
                val = float(val)
                
                anaylze_add_add_to_buffers(val)

            except:
                print("[mqtt handler] Error in parsing value: " + data.get('val') + "...")

    if msg.topic == topic[1]:
        
        # print("$$$$$$$$$$$$$$$$$ RAW DATA $$$$$$$$$$$$$$$$$$$$$")
        # print(data)
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        cmd = data.get('cmd')
        sth_was_modified = False

        #### INTRODUCTION REQUEST
        if cmd == "introduction_request":
            introduction_response_send()
            print("[mqtt handler] Introduction sent...")

        #### INPUT ANALYZER COMMANDS

        if cmd == "change_sensor_minmax":
            min = float(data.get('min'))
            max = float(data.get('max'))
            variable_container.min_sensor_val = min
            variable_container.max_sensor_val = max
            variable_container.should_update_range = True
            update_input_settings()
            sth_was_modified = True

            print_cmd_status_2("input analyzer settings change", cmd, "min", variable_container.min_sensor_val, "max", variable_container.max_sensor_val)

        #### INPUT ANALYZER COMMANDS END
        
        #### MUSIC THEORY COMMANDS 

        if cmd == "change_scale":
            scale_name = data.get('scale_name')
            scale_type = data.get('scale_type')
            variable_container.scale_base_note = scale_name
            variable_container.scale_type = scale_type
            variable_container.should_change_scale = True
            update_settings()
            sth_was_modified = True

            print_cmd_status_2("music theory settings change", cmd, "name", variable_container.scale_base_note, "type", variable_container.scale_type)

        if cmd == "change_octave_range":
            start_octave = int(data.get('start_octave'))
            octave_nums = int(data.get('octave_nums'))
            variable_container.octave_start = start_octave
            variable_container.octave_nums = octave_nums
            variable_container.should_change_octave = True
            update_settings()
            update_input_settings()
            sth_was_modified = True

            print_cmd_status_2("music theory settings change", cmd, "start octave", variable_container.octave_start, "nums", variable_container.octave_nums)


        #### MUSIC THEORY COMMANDS END

        #### SOUND COMMANDS 
        if cmd == "change_sound_out_active":
            isactive = data.get('isactive')
            if isactive == "true":
                variable_container.is_sound_out_active = True
            else:
                variable_container.is_sound_out_active = False
            sth_was_modified = True

            print_cmd_status_1("sound settings change", cmd, "is active", variable_container.is_sound_out_active)



        if cmd == "change_sound_wavetype":
            type = data.get('wave_type')
            variable_container.sound_wave_type = type
            sth_was_modified = True

            print_cmd_status_1("sound settings change", cmd, "wave type", variable_container.sound_wave_type)
            

        
        if cmd == "change_sound_duration":
            duration = float(data.get('duration'))
            variable_container.sound_duration = duration
            sth_was_modified = True

            print_cmd_status_1("sound settings change", cmd, "duration", variable_container.sound_duration)


        #### SOUND COMMANDS END

        #### MIDI COMMANDS 
        if cmd == "change_midi_out_active":
            isactive = data.get('isactive')
            if isactive == "true":
                variable_container.is_midi_out_active = True
            else:
                variable_container.is_midi_out_active = False
            sth_was_modified = True

            print_cmd_status_1("midi settings change", cmd, "is active", variable_container.is_midi_out_active)
        #### MIDI COMMANDS END


        if sth_was_modified:
            introduction_response_send()
            sth_was_modified = False