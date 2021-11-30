from kivy.event import EventDispatcher
from kivy.properties import ListProperty
from orb.misc.channel import Channel


class Channels(EventDispatcher):

    channels = ListProperty([])

    def __init__(self, lnd):
        super(Channels, self).__init__(
            channels=[Channel(c) for c in lnd.get_channels()]
        )
        self.sort_channels()

    def sort_channels(self):
        self.channels = sorted(
            self.channels,
            key=lambda x: int(x.local_balance) / int(x.capacity),
            reverse=True,
        )

    def __len__(self):
        return len(self.channels)

    def __iter__(self):
        self.it = 0
        return self

    def __next__(self):
        if self.it < len(self):
            ret = self.channels[self.it]
            self.it += 1
        else:
            raise StopIteration
        return ret
