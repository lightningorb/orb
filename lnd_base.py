class LndBase:
    def get_alias_from_channel_id(self, chan_id):
        for channel in self.get_channels():
            if chan_id == channel.chan_id:
                return self.get_node_alias(channel.remote_pubkey)

    def get_channel_capacity(self, chan_id):
        for channel in self.get_channels():
            if chan_id == channel.chan_id:
                return channel.capacity

    def get_channel_remote_balance(self, chan_id):
        for channel in self.get_channels():
            if chan_id == channel.chan_id:
                return channel.remote_balance

    def get_channel_local_balance(self, chan_id):
        for channel in self.get_channels():
            if chan_id == channel.chan_id:
                return channel.local_balance

    def get_channel_pending_htlcs(self, chan_id):
        for channel in self.get_channels():
            if chan_id == channel.chan_id:
                pending_in = sum(
                    int(p.amount) for p in channel.pending_htlcs if p.incoming
                )
                pending_out = sum(
                    int(p.amount) for p in channel.pending_htlcs if not p.incoming
                )
                return dict(pending_in=pending_in, pending_out=pending_out)
