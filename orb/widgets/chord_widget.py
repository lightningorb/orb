import math
from collections import defaultdict
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from colour import Color as Colour


class ChordWidget(Widget):
    def __init__(self, channels, *args, **kwargs):
        super(ChordWidget, self).__init__(*args, **kwargs)

        self.channels = channels
        self.radius = 950

        matrix = self.get_matrix()

        return

        with self.canvas:
            offset = 0
            sec_w = 360 / len(channels)
            sec_w2 = 360 / len(channels) / 2.5
            cols = [*Colour("red").range_to("blue", len(channels))]
            chan_pos = {}
            for chan, col in zip(channels, cols):
                Color(rgb=col.rgb)
                self.chord = Line(
                    circle=(0, 0, self.radius, offset - sec_w2, offset + sec_w2),
                    width=5,
                    cap="none",
                )
                chan_pos[chan.chan_id] = offset
                offset += sec_w

            for chan, col in zip(channels, cols):
                if chan.chan_id == 781558153871622145:
                    Color(rgb=col.rgb)
                    out_chans = [x[1] for x in matrix if x[0] == chan.chan_id]
                    self.draw_channel_chords(chan, out_chans, col, chan_pos, matrix)

    def draw_channel_chords(self, chan, out_chans, col, chan_pos, matrix):
        offset = chan_pos[chan.chan_id]

        def offset_to_pos(offset):
            x = math.sin(offset / 360 * 3.14378 * 2) * self.radius
            y = math.cos(offset / 360 * 3.14378 * 2) * self.radius
            return (x, y)

        for out_chan in out_chans:
            if out_chan in chan_pos:
                x, y = offset_to_pos(offset)
                x1, y1 = offset_to_pos(chan_pos[out_chan])
                Line(points=[x, y, x1, y1])

    def get_matrix(self):
        matrix = defaultdict(int)
        from orb.store import model

        chan_ids = [c.chan_id for c in self.channels]
        for c in self.channels:
            hist = (
                model.FowardEvent()
                .select()
                .where(model.FowardEvent.chan_id_out == c.chan_id)
            )
            for h in hist:
                matrix[(h.chan_id_out, h.chan_id_in)] += h.amt_out

        return matrix

    def print_matrix(self, chan_ids, matrix):
        for ci in chan_ids:
            for cj in chan_ids:
                if ci != cj:
                    print(f"{matrix[(ci, cj)]:<10}", end="")
            print("")
