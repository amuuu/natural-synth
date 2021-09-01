from flask import Blueprint, render_template, Response, request
from flask_login import login_required, current_user
from . import db

from . import mqtthandler

import json

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    return render_template('index.html', email=current_user.email)

@main.route('/nodes', methods=['GET'])
def node_divs():
    return render_template('nodediv.html', node_info=mqtthandler.divs)

@main.route('/changename', methods=['POST'])
def change_name():
    try:
        data = request.json
        new_name = data.get('Data').get('new_name')
        device_name = data.get('Data').get('device_name')

        mqtthandler.peripheral_node_name_update(device_name, new_name)
    except:
        return Response("Error in changing name.", status=400)

    return Response("Name changed successfully.", status=200)

@main.route('/changeactiveself', methods=['POST'])
def change_activeself():
    try:
        data = request.json
        device_name = data.get('Data').get('device_name')
        activeself = data.get('Data').get('activeself')
        mqtthandler.peripheral_node_activeself_update(device_name, activeself)
    
    except:
        return Response("Error in changing activeself.", status=400)

    return Response("Activeself changed successfully.", status=200)


@main.route('/peripheral_introductionrequest', methods=['GET'])
def peripheral_introduction_request():
    try:
        mqtthandler.peripheral_introduction_request()
        return Response("Sent peripherals introduction request successfully.", status=200)
    except:
        return Response("Error in sending peripherals introduction request.", status=400)

@main.route('/raspberry_introductionrequest', methods=['GET'])
def raspberry_introduction_request():
    try:
        mqtthandler.processing_node_introduction_request()
        return Response("Sent raspberry introduction request successfully.", status=200)
    except:
        return Response("Error in sending raspberry introduction request.", status=400)

@main.route('/get_raspberry_info', methods=['GET'])
def get_raspberry_info():
    return render_template('synthsettingsform.html', info=mqtthandler.raspberry_info_dict)


@main.route('/changeraspbberysettings', methods=['POST'])
def change_raspberrysettings():
    try:
        data = request.json
        
        max_sensor_val = data.get('Data').get('max_sensor_val')
        min_sensor_val = data.get('Data').get('min_sensor_val')
        
        if mqtthandler.raspberry_info_dict['max_sensor_val'] != max_sensor_val or\
             mqtthandler.raspberry_info_dict['min_sensor_val'] != min_sensor_val:
            mqtthandler.processing_node_change_sensor_minmax(min_sensor_val, max_sensor_val)

        scale_type = data.get('Data').get('scale_type')
        scale_base_note = data.get('Data').get('scale_base_note')

        if mqtthandler.raspberry_info_dict['scale_type'] != scale_type or\
            mqtthandler.raspberry_info_dict['scale_base_note'] != scale_base_note:
            mqtthandler.processing_node_change_scale(scale_base_note, scale_type)

        octave_start = data.get('Data').get('octave_start')
        octave_nums = data.get('Data').get('octave_nums')

        if mqtthandler.raspberry_info_dict['octave_start'] != octave_start or\
            mqtthandler.raspberry_info_dict['octave_nums'] != octave_nums:
            mqtthandler.processing_node_change_octave_range(octave_start,octave_nums)

        is_sound_out_active_str = data.get('Data').get('is_sound_out_active')
        if is_sound_out_active_str == "true":
            is_sound_out_active = True
        else:
            is_sound_out_active = False

        if mqtthandler.raspberry_info_dict['is_sound_out_active'] != is_sound_out_active:
            mqtthandler.processing_node_change_sound_out_active(is_sound_out_active_str)

        is_midi_out_active_str = data.get('Data').get('is_midi_out_active')
        if is_midi_out_active_str == "true":
            is_midi_out_active = True
        else:
            is_midi_out_active = False
        
        if mqtthandler.raspberry_info_dict['is_midi_out_active'] != is_midi_out_active:
             mqtthandler.processing_node_change_midi_out_active(is_midi_out_active_str)
        
        sound_wave_type = data.get('Data').get('sound_wave_type')
        if mqtthandler.raspberry_info_dict['sound_wave_type'] != sound_wave_type:
            mqtthandler.processing_node_change_sound_wavetype(sound_wave_type)

        sound_duration = data.get('Data').get('sound_duration')
        if mqtthandler.raspberry_info_dict['sound_duration'] != sound_duration:
            mqtthandler.processing_node_change_sound_duration(sound_duration)
         
    except:
        return Response("Error in changing raspberry settings.", status=400)

    return Response("Raspberry settings changed successfully.", status=200)
