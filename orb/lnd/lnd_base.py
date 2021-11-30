import codecs


class LndBase:
    def get_alias_from_channel_id(self, chan_id):
        for channel in self.get_channels():
            if chan_id == channel.chan_id:
                return self.get_node_alias(channel.remote_pubkey)

    @staticmethod
    def hex_string_to_bytes(hex_string):
        decode_hex = codecs.getdecoder("hex_codec")
        return decode_hex(hex_string)[0]
