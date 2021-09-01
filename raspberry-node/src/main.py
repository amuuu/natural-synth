import random
from flask import Blueprint
from flask.globals import request
from . import soundhandler, musictheoryhandler, variable_container, inputanalyzer

main = Blueprint('main', __name__)
is_debug_init_done__soundhandler = False
is_debug_init_done__inputanalyzer = False


@main.route('/')
def flask_check():
    print("Flask is running...")
    return "<h1>Flask is running...</h1>"

@main.route('/random')
def debug__play_random_note():
    global is_debug_init_done__soundhandler
    if not is_debug_init_done__soundhandler:
        musictheoryhandler.init() 
        is_debug_init_done__soundhandler = True

    random_index = musictheoryhandler.get_random_note_index_in_scale()
    note = musictheoryhandler.quantize_note(random_index)
    note_in_octave = musictheoryhandler.get_note_in_octave_range(musictheoryhandler._notes.index(musictheoryhandler._scale_base_note_current) + note)
    soundhandler.add_to_soundbuffer(note_in_octave,variable_container.sound_duration,1,variable_container.sound_wave_type)
    
    resp = "<h1>debug__random note</h1><br><br><h3>played the note number %s (%s)</h3>" % (note_in_octave, musictheoryhandler.note_number_to_name(note_in_octave))
    return resp

#/random_seq?length=10
@main.route('/random_seq')
def debug__play_random_note_seq():
    global is_debug_init_done__soundhandler
    if not is_debug_init_done__soundhandler:
        musictheoryhandler.init() 
        is_debug_init_done__soundhandler = True
    
    length = request.args.get('length', default = 1, type = int)
    print(musictheoryhandler._scale_notes_current)
    for i in range(length):
        random_index = musictheoryhandler.get_random_note_index_in_scale()
        note = musictheoryhandler.quantize_note(random_index)
        note_in_octave = musictheoryhandler.get_note_in_octave_range(musictheoryhandler._notes.index(musictheoryhandler._scale_base_note_current) + note)
        soundhandler.add_to_soundbuffer(note_in_octave,variable_container.sound_duration,1,variable_container.sound_wave_type)
    
    resp = "<h1>debug__random sequnce</h1>"
    return resp

#/rawval_test?val=132
@main.route('/rawval_test')
def debug__raw_val_to_note():
    global is_debug_init_done__soundhandler
    if not is_debug_init_done__soundhandler:
        musictheoryhandler.init() 
        is_debug_init_done__soundhandler = True
    global is_debug_init_done__inputanalyzer
    if not is_debug_init_done__inputanalyzer:
        inputanalyzer.init() 
        is_debug_init_done__inputanalyzer = True
    
    val = request.args.get('val', default = 120, type = float)
    print("Recieved val " + str(val) + "... Analyzing now...")
    processed_note_num = inputanalyzer.anaylze_add_add_to_buffers(val)

    if processed_note_num != -1:
        resp = "<h1>Analyzed the raw value of %s.</h1><h2>It was turned into note %s (%s). </h2>" % (val, processed_note_num, musictheoryhandler.note_number_to_name(processed_note_num))
    else:
        resp = "<h1>Analyzed the raw value of %s.</h1><h2>It was out of sensor value range and was ignored. </h2>" % (val)
    return resp