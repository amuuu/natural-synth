import threading
import time

from . import midihandler
from .variable_container import sound_duration as duration

class MidiOutThread(threading.Thread):   
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        print("[midi out thread] Initialized...")

    def run(self):
        print("[midi out thread] Running...")
        
        while True:
            try:
                if len(midihandler.midi_buffer) != 0:
                    midi_note = midihandler.midi_buffer.pop(0)
                    print("[midi out thread] Sending note " + str(midi_note) + "...")
                    MidiNoteSignal(midihandler.midiout, midi_note, duration).start()
            finally:
                pass

class MidiNoteSignal(threading.Thread):
    def __init__(self, midiout, value, delay):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.midiout = midiout
        self.value = value
        self.delay = delay

    def run(self):
        try:
            with self.midiout:
                print("[midi out thread] Sent signal...")
                note_on = [0x90, self.value, 112]
                note_off = [0x80, self.value, 0]
                self.midiout.send_message(note_on)
                time.sleep(self.delay)
                self.midiout.send_message(note_off)
                time.sleep(0.2)
            
            midihandler.re_init()
            
        finally:
            self._stop_event.set()