from . import variable_container

import random
import math


_notes = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]

_major_scale_notes = [0,2,4,5,7,9,11]
_major_scale_chords = ['M', 'm', 'm', 'M', 'M', 'm', 'dim']
_major_scale_chord_progressions = [[1,4,5], [1,5,6,4], [2,5,1], [1,6,4,5], [1,4,5,4]] # -1 the index

_minor_harmonic_scale_notes = [0,2,3,5,7,8,11]
_minor_harmonic_scale_chords = ['m', 'dim', 'aug', 'm', 'M', 'M', 'dim']
_minor_harmonic_scale_chord_progressions = [[1,4,5], [1,2,5,1]]

_OCTAVE_NOTES_NUM = 12
_SCALE_NOTES_NUM = 7

_note_index_last = 2


def init():
    _set_scale()
    _update_data_shrink_range()

def update_settings():
    
    if variable_container.should_update_range:
        _update_data_shrink_range()
        variable_container.should_update_range = False

    if variable_container.should_change_scale:
        _set_scale()
        variable_container.should_change_scale = False

    if variable_container.should_change_octave:
        _update_octave_range()
        variable_container.should_change_octave = False
        
    if variable_container.should_change_chord_mode:
        pass



def convert_data_to_note(raw_data):
    number = _process_raw_data(raw_data)

    if not variable_container.is_chord_mode:
        note = _quantize_note(number)
        return _get_note_in_octave_range(_notes.index(_scale_base_note_current) + note)


def _set_scale():
    global _scale_notes_current
    global _scale_type_current
    global _scale_base_note_current

    if variable_container.scale_type == 'major':
        _scale_notes_current = _major_scale_notes
        _scale_type_current = 'major'
        _scale_base_note_current = variable_container.scale_base_note
    
    elif variable_container.scale_type == 'minor':
        _scale_notes_current = _minor_harmonic_scale_notes
        _scale_type_current = 'minor'
        _scale_base_note_current = variable_container.scale_base_note

def _get_note_in_octave_range(note):
    _update_octave_range()

    target_octave = random.randint(_octave_start, _octave_end)
    
    return note + target_octave * _OCTAVE_NOTES_NUM

def _quantize_note(note):
    
    mod = note % _SCALE_NOTES_NUM
    
    current_base_note = _notes.index(_scale_base_note_current)
    
    closest_index, count = 0, 0
    diff = 1000
    for n in _scale_notes_current:
        if (n + current_base_note) == mod:
            return mod
        
        else:
            if math.floor(n + current_base_note - mod) < diff:
                diff = math.floor(n + current_base_note - mod)
                closest_index = count
        
        count+=1
    
    return _scale_notes_current[closest_index]

def _process_raw_data(data):
    return data * _raw_data_shrink_factor + _raw_data_shrink_offset

def _update_data_shrink_range():
    global _raw_data_shrink_factor
    global _raw_data_shrink_offset

    sensor_val_diff = variable_container.max_sensor_val - variable_container.min_sensor_val
    notes_num = variable_container.octave_nums * _SCALE_NOTES_NUM
    
    alpha = sensor_val_diff / notes_num
    
    if sensor_val_diff > notes_num:
        _raw_data_shrink_factor = 1 / alpha
        _raw_data_shrink_offset = (alpha * variable_container.min_sensor_val - variable_container.octave_start * _OCTAVE_NOTES_NUM) * -1
    else:
        _raw_data_shrink_factor = alpha
        _raw_data_shrink_offset = variable_container.min_sensor_val - alpha
    
def _update_octave_range():
    global _octave_start
    global _octave_end
    global _octave_nums

    _octave_start = variable_container.octave_start
    _octave_end = variable_container.octave_start + variable_container.octave_nums - 1
    _octave_nums = variable_container.octave_nums

def _get_random_note_index_in_scale():
    global _note_index_last
    
    note_index_new = random.randint(0,_SCALE_NOTES_NUM-1)
    if note_index_new == _note_index_last:
        if not variable_container.can_play_conescutive_repeating_notes:
            while note_index_new == _note_index_last:
                note_index_new = random.randint(0,_SCALE_NOTES_NUM-1)
    _note_index_last = note_index_new
    return note_index_new
