from collections import defaultdict


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
