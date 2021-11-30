from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.properties import BooleanProperty
from kivy.event import EventDispatcher


class Channel(EventDispatcher):
    capacity = NumericProperty(0)
    remote_pubkey = StringProperty("")
    local_balance = NumericProperty(0)
    remote_balance = NumericProperty(0)
    chan_id = NumericProperty(0)
    pending_htlcs = ListProperty([])
    total_satoshis_sent = NumericProperty(0)
    total_satoshis_received = NumericProperty(0)
    unsettled_balance = NumericProperty(0)
    commit_fee = NumericProperty(0)
    initiator = BooleanProperty(False)

    def __init__(self, channel, *args, **kwargs):
        super(Channel, self).__init__(*args, **kwargs)
        self.local_balance = channel.local_balance
        self.capacity = channel.capacity
        self.remote_pubkey = channel.remote_pubkey
        self.local_balance = channel.local_balance
        self.remote_balance = channel.remote_balance
        self.chan_id = channel.chan_id
        self.pending_htlcs = channel.pending_htlcs
        self.total_satoshis_sent = channel.total_satoshis_sent
        self.total_satoshis_received = channel.total_satoshis_received
        self.ListFields = channel.ListFields
        self.initiator = channel.initiator
        self.commit_fee = channel.commit_fee
        self.unsettled_balance = channel.unsettled_balance
        self.channel_point = channel.channel_point
