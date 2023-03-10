# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-07-23 16:57:28

from orb.misc.utils import pref
from kivy.core.audio import SoundLoader


class AudioManager:

    """
    The AudioManager class should encapsulate all playback
    functionality.
    """

    def __init__(self):
        """
        Class constructor.
        """
        self.volume = 1
        self._current_sound = None
        self.send = SoundLoader.load("orb/audio/send_settle.ogg")
        self.forward = SoundLoader.load("orb/audio/forward_settle.ogg")
        self.link_fail = SoundLoader.load("orb/audio/link_fail_event.ogg")

    def play(self, sound):
        if self._current_sound:
            self._current_sound.stop()
            self._current_sound = None
        self._current_sound = sound
        sound.volume = float(pref("audio.volume"))
        sound.play()

    def play_send_settle(self):
        """
        Play the audio for send HTLC.
        """
        self.play(self.send)

    def play_forward_settle(self):
        """
        Play the audio for forward HTLC.
        """
        self.play(self.forward)

    def play_link_fail_event(self):
        """
        Play the audio for failed HTLC.
        """
        self.play(self.link_fail)


audio_manager = AudioManager()
