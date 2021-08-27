from synthesizer import Player, Synthesizer, Waveform
import math


sound_buffer = []
_waveform_name_obj_dict = {}

def init():
    _init_waveform_name_to_obj_dict()

def play(note, duration, volume, waveform_type):
    player = Player()
    player.open_stream()
    synthesizer = Synthesizer(osc1_waveform=_waveform_name_obj_dict[waveform_type], osc1_volume=volume, use_osc2=False)
    player.play_wave(synthesizer.generate_constant_wave(_note_to_frequency(note), duration))
    #time.sleep(duration)

def _note_to_frequency(note):
    const = 1.059463
    base_freq = 440.0
    distance_to_basenote = note - 57
    res = base_freq * math.pow(const, distance_to_basenote)
    return res

def _init_waveform_name_to_obj_dict():
    _waveform_name_obj_dict['sine'] = Waveform.sine
    _waveform_name_obj_dict['triangle'] = Waveform.triangle
    _waveform_name_obj_dict['square'] = Waveform.square
    _waveform_name_obj_dict['saw'] = Waveform.sawtooth

def add_to_soundbuffer(sound_object):
    global _waveform_name_obj_dict
    global sound_buffer

    sound_buffer.extend(sound_object)

class SoundObject:
    def __init__(self, note_num, duration, volume, waveform_type):
        self.note_num = note_num
        self.duration = duration
        self.volume = volume
        self.waveform_type = waveform_type