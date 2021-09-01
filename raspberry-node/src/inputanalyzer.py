from . import variable_container
from .musictheoryhandler import quantize_note, _SCALE_NOTES_NUM
from .soundhandler import add_to_soundbuffer
from .midihandler import add_to_midibuffer
from .util import print_tmp

def init():
    _update_data_shrink_range()

def update_input_settings():
    
    if variable_container.should_update_range:
        _update_data_shrink_range()
        variable_container.should_update_range = False

def anaylze_add_add_to_buffers(val):
    
    if not variable_container.is_sound_out_active and not variable_container.is_midi_out_active:
        return -1
    
    note_num = _convert_data_to_note(val)

    if note_num == -1:
        return -1

    if variable_container.is_sound_out_active:
        add_to_soundbuffer(note_num,variable_container.sound_duration,1,variable_container.sound_wave_type)

    if variable_container.is_midi_out_active:
        add_to_midibuffer(note_num)

    return note_num

def _update_data_shrink_range():
    global _raw_data_shrink_factor
    global _raw_data_shrink_offset

    sensor_val_diff = variable_container.max_sensor_val - variable_container.min_sensor_val
    notes_num = variable_container.octave_nums * _SCALE_NOTES_NUM
    
    alpha = sensor_val_diff / notes_num
    
    if sensor_val_diff > notes_num:
        _raw_data_shrink_factor = 1 / alpha
        _raw_data_shrink_offset = int((_raw_data_shrink_factor * variable_container.min_sensor_val) * -1)
    else:
        _raw_data_shrink_factor = alpha
        _raw_data_shrink_offset = int((_raw_data_shrink_factor * variable_container.min_sensor_val) * -1)

    print_tmp(["sensor_val_diff"], [sensor_val_diff])
    print_tmp(["notes_num"], [notes_num])
    print_tmp(["_raw_data_shrink_factor"], [_raw_data_shrink_factor])
    print_tmp(["_raw_data_shrink_offset"], [_raw_data_shrink_offset])

def _convert_data_to_note(raw_data):
    
    print_tmp(["raw data"], [raw_data])

    number = int(_process_raw_data(raw_data))
    
    print_tmp(["processed raw data"], [number])
    
    if number == -1:
        return -1

    if not variable_container.is_chord_mode:
        note = quantize_note(number)
        print_tmp(["quantized note"], [note])

        return note

def _process_raw_data(data):
    if data < variable_container.min_sensor_val or data > variable_container.max_sensor_val:
        print("Raw sensor value outside defined range... So it got ignored.")
        return -1

    return data * _raw_data_shrink_factor + _raw_data_shrink_offset
