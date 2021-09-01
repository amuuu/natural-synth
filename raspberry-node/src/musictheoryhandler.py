from os import close
from . import variable_container
from .util import print_tmp

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

def update_settings():
    
    if variable_container.should_change_scale:
        _set_scale()
        variable_container.should_change_scale = False

    if variable_container.should_change_octave:
        _update_octave_range()
        variable_container.should_change_octave = False
        
    if variable_container.should_change_chord_mode:
        pass

def get_note_in_random_octave_in_range(note):
    _update_octave_range()

    target_octave = random.randint(_octave_start, _octave_end)
    
    return note + target_octave * _OCTAVE_NOTES_NUM

def quantize_note(note):
    
    octave = int(note/_SCALE_NOTES_NUM)
    mod = note % _SCALE_NOTES_NUM
    current_base_note = _notes.index(_scale_base_note_current)

    return (_scale_notes_current[mod] + current_base_note) + ((octave + variable_container.octave_start + 1) * _OCTAVE_NOTES_NUM)

def shift_note_in_scale(note):
    return _notes.index(_scale_base_note_current) + note

def get_random_note_index_in_scale():
    global _note_index_last
    
    note_index_new = random.randint(0,_SCALE_NOTES_NUM-1)
    while note_index_new == _note_index_last:
        note_index_new = random.randint(0,_SCALE_NOTES_NUM-1)
    _note_index_last = note_index_new
    return _scale_notes_current[note_index_new]+_notes.index(_scale_base_note_current)

def note_number_to_name(note):
    return _notes[note%_OCTAVE_NOTES_NUM].upper()+str(int(note/_OCTAVE_NOTES_NUM - 1))

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

def _update_octave_range():
    global _octave_start
    global _octave_end
    global _octave_nums

    _octave_start = variable_container.octave_start
    _octave_end = variable_container.octave_start + variable_container.octave_nums - 1
    _octave_nums = variable_container.octave_nums
