import threading

from . import soundhandler

class SoundOutThread(threading.Thread):   
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()

    def run(self):
        while True:
            try:
                if len(soundhandler.sound_buffer) != 0:
                    sound_object = soundhandler.sound_buffer.pop(0)
                    print("[sound out thread] Playing note " + str(sound_object.note_num) + "...")
                    soundhandler.play(sound_object.note_num, sound_object.duration, sound_object.volume, sound_object.waveform_type)
            finally:
                pass