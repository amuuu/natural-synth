import rtmidi

from .variable_container import midiout_channel, midiout_port

midi_buffer = []

FIRST_TIME_LOADING_PORTS = True

def init():
    global midiout
    global available_ports
    global FIRST_TIME_LOADING_PORTS

    midiout = rtmidi.MidiOut()
    available_ports = midiout.get_ports()
    
    if FIRST_TIME_LOADING_PORTS:
        print(available_ports)
        FIRST_TIME_LOADING_PORTS = False
    
    if available_ports:
        try:
            midiout.open_port(midiout_port)
        except:
            print("[midi handler] Not a valid MIDI port. Connected to a virtual port instead.")
            midiout.open_virtual_port("Virtual Output")
    else:
        midiout.open_virtual_port("Virtual Output")


def add_to_midibuffer(midi_note):
    midi_buffer.append(midi_note)

def re_init():
    global midiout

    del midiout
    init()