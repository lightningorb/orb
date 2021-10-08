try:
    from kivy.core.audio import SoundLoader
except:
    pass


class AudioManager:
    send_settle = SoundLoader.load("audio/send_settle.wav")
    forward_settle = SoundLoader.load("audio/forward_settle.wav")

    def play_send_settle(self):
        try:
            self.send_settle.play()
        except:
            pass

    def play_forward_settle(self):
        try:
            self.forward_settle.play()
        except:
            pass


audio_manager = AudioManager()
