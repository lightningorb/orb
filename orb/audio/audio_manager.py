# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-01-16 06:28:21
from kivy.utils import platform
from orb.misc.utils import pref

# ios = platform == "ios"
ios = False


class AudioManager:

    """
    The AudioManager class should encapsulate all playback
    functionality.
    """

    def __init__(self):
        """
        Class constructor.
        """
        if not ios:
            from kivy.core.audio import SoundLoader

            self.send_settle = SoundLoader.load("orb/audio/send_settle.wav")
            self.forward_settle = SoundLoader.load("orb/audio/forward_settle.wav")
            self.link_fail_event = SoundLoader.load("orb/audio/link_fail_event.wav")
            self.samples = [self.send_settle, self.forward_settle, self.link_fail_event]

    def set_volume(self):
        """
        Sets the volume based on the application settings.
        """
        if not ios:
            for sample in self.samples:
                sample.volume = pref("audio.volume")

    def play(self, sound):
        if not ios:
            if sound.state == "play":
                sound.stop()
            sound.seek(0)
            sound.play()

    def play_send_settle(self):
        """
        Play the audio for send HTLC.
        """
        self.play(self.send_settle)

    def play_forward_settle(self):
        """
        Play the audio for forward HTLC.
        """
        self.play(self.forward_settle)

    def play_link_fail_event(self):
        """
        Play the audio for failed HTLC.
        """
        self.play(self.link_fail_event)


audio_manager = AudioManager()
