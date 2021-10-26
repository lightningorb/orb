import data_manager
from ui_actions import console_output
from threading import Thread

def get_forwarding_history():
    from store import model
    return model.FowardEvent().select()# .where(model.FowardEvent.chan_id_in == '772380530381488129')

def download_forwarding_history():
    def func():
        from store import model
        console_output('downloading forwarding history')
        last = model.FowardEvent.select().order_by(model.FowardEvent.timestamp_ns.desc()).first()
        lnd = data_manager.data_man.lnd
        i = 0
        while True:
            console_output(f'fetching events {i} -> {i + 100}')
            fwd = lnd.get_forwarding_history(
                start_time=(last.timestamp_ns+1 if last else None),
                index_offset=i,
                num_max_events=100)

            for f in fwd.forwarding_events:
                ev = model.FowardEvent(
                    timestamp = int(f.timestamp),
                    chan_id_in = int(f.chan_id_in),
                    chan_id_out = int(f.chan_id_out),
                    amt_in = int(f.amt_in),
                    amt_out = int(f.amt_out),
                    fee = int(f.fee),
                    fee_msat = int(f.fee_msat),
                    amt_in_msat = int(f.amt_in_msat),
                    amt_out_msat = int(f.amt_out_msat),
                    timestamp_ns = int(f.timestamp_ns))
                ev.save()
            i += 100
            if not fwd.forwarding_events:
                break
        console_output('downloaded forwarding history')
    Thread(target=func).start()

def clear_forwarding_history():
    from store import model
    model.FowardEvent.delete().execute()

def view_forwarding_history():
    from kivy.uix.popup import Popup
    from kivy.uix.label import Label
    from data_manager import data_man
    import requests

    fh = get_forwarding_history()

    total_out = 0
    total_in = 0
    total_fee = 0

    for f in fh.iterator():
        total_out += f.amt_out
        total_in += f.amt_in
        total_fee += f.fee

    text = f"""
    Satoshis:

    total fees: s{total_fee:,}
    total out: s{total_out:,} 
    total in: s{total_in:,}
    """

    popup = Popup(title='Total Routing',
        content=Label(text=text),
        size_hint=(None, None), size=(500, 400))
    popup.open()