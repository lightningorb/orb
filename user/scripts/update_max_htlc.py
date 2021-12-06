import data_manager

lnd = data_manager.data_man.lnd

from threading import Thread
from orb.misc.ui_actions import console_output


def update_max_htlc(*args):
    for i, c in enumerate(lnd.get_channels()):
        print(f"Updating policy for: {c.chan_id}")
        console_output(f"Updating policy for: {c.chan_id}")
        policy = lnd.get_policy_to(c.chan_id)
        lnd.update_channel_policy(
            channel=c,
            time_lock_delta=int(policy.time_lock_delta),
            fee_rate=int(policy.fee_rate_milli_msat) / 1e6,
            base_fee_msat=int(policy.fee_base_msat),
            max_htlc_msat=int(c.local_balance / 5) * 1000,
        )


def main():
    Thread(target=update_max_htlc).start()
