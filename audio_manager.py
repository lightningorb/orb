from kivy.utils import platform
from utils import pref

ios = platform == 'ios'

class AudioManager:
    def __init__(self):
        if not ios:
            from kivy.core.audio import SoundLoader
            self.send_settle = SoundLoader.load("audio/send_settle.wav")
            self.forward_settle = SoundLoader.load("audio/forward_settle.wav")
            self.link_fail_event = SoundLoader.load("audio/link_fail_event.wav")
            self.samples = [self.send_settle, self.forward_settle, self.link_fail_event]

    def set_volume(self):
        if not ios:
            for sample in self.samples:
                sample.volume = pref('audio.volume')

    def play_send_settle(self):
        if not ios:
            self.send_settle.play()

    def play_forward_settle(self):
        if not ios:
            self.forward_settle.play()

    def play_link_fail_event(self):
        if not ios:
            self.link_fail_event.play()


audio_manager = AudioManager()
