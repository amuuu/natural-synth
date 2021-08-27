import random
from flask import Blueprint
from flask.globals import request
from . import soundhandler, musictheoryhandler, variable_container

main = Blueprint('main', __name__)
is_debug_init_done = False

@main.route('/')
def flask_check():
    print("Flask is running...")
    return "<h1>Flask is running...</h1>"

@main.route('/random')
def debug__play_random_note():
    global is_debug_init_done
    if not is_debug_init_done:
        musictheoryhandler.init() 
        is_debug_init_done = True

    random_index = musictheoryhandler._get_random_note_index_in_scale()
    note = musictheoryhandler._quantize_note(random_index)
    note_in_octave = musictheoryhandler._get_note_in_octave_range(musictheoryhandler._notes.index(musictheoryhandler._scale_base_note_current) + note)
    soundhandler.add_to_soundbuffer(note_in_octave,variable_container.sound_duration,1,variable_container.sound_wave_type)
    
    resp = "<h1>debug__random note</h1><br><br><h3>played the note number %s</h3>" % note_in_octave
    return resp

#/random_seq?length=10
@main.route('/random_seq')
def debug__play_random_note_seq():
    global is_debug_init_done
    if not is_debug_init_done:
        musictheoryhandler.init() 
        is_debug_init_done = True
    
    length = request.args.get('length', default = 1, type = int)
    print(musictheoryhandler._scale_notes_current)
    for i in range(length):
        random_index = musictheoryhandler._get_random_note_index_in_scale()
        note = musictheoryhandler._quantize_note(random_index)
        print("raw: " + str(random_index) + " quan: " + str(note))

        note_in_octave = musictheoryhandler._get_note_in_octave_range(musictheoryhandler._notes.index(musictheoryhandler._scale_base_note_current) + note)
        soundhandler.add_to_soundbuffer(note_in_octave,variable_container.sound_duration,1,variable_container.sound_wave_type)
    
    resp = "<h1>debug__random sequnce</h1>"
    return resp

