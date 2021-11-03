from collections import defaultdict
import json
from ui_actions import console_output


def get_payments():
    from store import model

    return model.Payment().select()


def print_logs():
    payments = get_payments()
    for r in payments.iterator():
        if not r.succeeded:
            continue
        print('=====================')
        print(f'Payment of {r.amount} to {lnd.get_node_alias(r.dest)}')
        print(r.amount, r.dest, r.fees, r.succeeded)
        for a in r.attempts:
            print('----------')
            print('Attempt:')
            prev = None
            for h in a.hops:
                if prev:
                    print(
                        f'{lnd.get_node_alias(prev.pk)} -> {lnd.get_node_alias(h.pk)}'
                    )
                prev = h
            if a.succeeded:
                print("SUCCESS!")
            else:
                print(
                    f'Failed with code: {a.code} at'
                    f' {lnd.get_node_alias(a.weakest_link_pk)}'
                )


def export(path):
    payments = []
    hops = []
    for r in get_payments().iterator():
        if not r.succeeded:
            continue
        attempts = []
        for a in r.attempts:
            hops = []
            for h in a.hops:
                data = h.__data__
                del data['id']
                del data['attempt']
                hops.append(dict(data=data))
            data = a.__data__
            del data['id']
            del data['payment']
            attempts.append(dict(data=data, hops=hops))
        data = r.__data__
        del data['id']
        payments.append(dict(data=data, attempts=attempts))
    with open(path, 'w') as f:
        f.write(json.dumps(payments, indent=4))
    console_output(f'exported to: {path}')


def ingest(path):
    from store import model

    console_output(f'Ingesting {path}')

    with open(path, 'r') as f:
        payments = json.loads(f.read())
        for p in payments:
            payment = model.Payment(**p['data'])
            payment.save()
            for a in p['attempts']:
                attempt = model.Attempt(**a['data'], payment=payment)
                attempt.save()
                for h in a['hops']:
                    hop = model.Hop(**h['data'], attempt=attempt)
                    hop.save()
    console_output('Ingestion done. Re-open the Rankings window.')


def count_successes_failures():
    import data_manager

    lnd = data_manager.data_man.lnd
    payments = get_payments()
    nodes = defaultdict(lambda: dict(successes=0, failures=0))
    for r in payments.iterator():
        if not r.succeeded:
            continue
        for a in r.attempts.iterator():
            if a.succeeded:
                for hop in a.hops.iterator():
                    nodes[hop.pk]['successes'] += 1
            elif a.code == 15:
                nodes[a.weakest_link_pk]['failures'] += 1
    return sorted(
        [
            [
                lnd.get_node_alias(node),
                nodes[node]["successes"],
                nodes[node]["failures"],
            ]
            for node in nodes
        ],
        key=lambda x: x[1],
        reverse=True,
    )


def ingest_db(path):
    pass
