# -*- coding: utf-8 -*-
# @Author: lnorb.com
# @Date:   2021-12-15 07:15:28
# @Last Modified by:   lnorb.com
# @Last Modified time: 2022-02-01 06:39:01

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
        self.play(SoundLoader.load("orb/audio/send_settle.wav"))

    def play_forward_settle(self):
        """
        Play the audio for forward HTLC.
        """
        self.play(SoundLoader.load("orb/audio/forward_settle.wav"))

    def play_link_fail_event(self):
        """
        Play the audio for failed HTLC.
        """
        self.play(SoundLoader.load("orb/audio/link_fail_event.wav"))


audio_manager = AudioManager()
