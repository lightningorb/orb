### 2022-02-05 13:59:39.890046: clock-out


### 2022-02-05 13:44:47.727372: clock-in

### 2022-01-23 15:48:14.240432: clock-out

* using last_offset_index from lnd, still getting discrepancy
<!-- #region -->
Writing forwarding events to log file. Run the following from the Orb console
```python
from orb.store import model

with open('forwarding_events.csv', 'w') as f:
	f.write('timestamp_ns,amt_in,amt_out,fee\n') 
	for event in model.ForwardEvent().select():
		f.write('{},{},{},{}\n'.format(event.timestamp_ns, event.amt_in, event.amt_out, event.fee))
print('wrote events to forwarding_events.csv')
```
<!-- #endregion -->

<!-- #region -->
Direct from LND

```python
print('\n\nopening forwarding_events_lnd.csv')
with open('forwarding_events_lnd.csv', 'w') as file_:
	i = 0
	file_.write('timestamp_ns,amt_in,amt_out,fee\n')
	while True:
		fwd = Lnd().get_forwarding_history(start_time=None, index_offset=i, num_max_events=100)
		print('got forwarding history')
		for j, f in enumerate(fwd.forwarding_events):
			file_.write('{},{},{},{}\n'.format(f.timestamp_ns, f.amt_in, f.amt_out, f.fee))
		i = fwd.last_offset_index
		print('last index: {}'.format(i))
		if not fwd.forwarding_events:
			break
print('wrote forwarding_events_lnd.csv\n\n\n')
```
<!-- #endregion -->

```python
import numpy as np
import pandas as pd
```

```python
fwd = pd.read_csv('../forwarding_events_lnd.csv', index_col=0)
fwd.index = pd.to_datetime(fwd.index)
```

```python
fwd['amt_delta'] = fwd.amt_in - fwd.amt_out
```

```python
fwd[fwd.amt_delta != fwd.fee]
```

These amounts still aren't adding up when pulling from the database.

```python
fwd.sum() # matches what is shown in Total Routing dialogue
```

```python
(fwd.amt_in - fwd.amt_out).sum() # 968
```

```python
fwd.fee.sum() # 965
```

* renaming foward->forward
Reconnecting to playground


### 2022-01-23 13:37:16.617105: clock-in

### 2022-01-22 16:01:13.079311: clock-out

```python
import numpy as np
```

<!-- #region -->
To generate forwarding history:

```python
from orb.store import model
for event in model.FowardEvent().select():
    print(f'{event.chan_id_in} -> {event.chan_id_out} {event.amt_out} forwarded')
```
<!-- #endregion -->

<details> <summary> Getting my forwarding history from dump </summary>

```python
# in, out, fees:
forwarded = [
    [100002, 100001, 1],
    [100002, 100001, 1],
    [100002, 100001, 1],
    [83176, 83099, 76],
    [46214, 46171, 43],
    [40875, 40836, 38],
    [88337, 88242, 95],
    [76448, 76447, 1],
    [86331, 86238, 93],
    [88644, 88563, 81],
    [79388, 79315, 73],
    [69959, 69958, 1],
    [94446, 94445, 1],
    [84659, 84581, 78],
    [83300, 83224, 76],
    [73685, 73617, 68],
    [52340, 52339, 1],
    [67805, 67742, 62],
    [66421, 66360, 61],
    [85990, 85911, 79],
    [86428, 86427, 1],
    [85619, 85618, 1],
    [36576, 36575, 1],
    [48726, 48725, 1],
    [44237, 44236, 1],
    [45302, 45301, 1],
    [50419, 50418, 1],
    [55957, 55956, 1],
    [35805, 35804, 1],
    [26210, 26209, 1],
    [90652, 90651, 1],
    [8573, 8572, 1],
]
forwarded = np.array(forwarded)
```

</details>

```python
np.array([('a', 'b', 'c')])
```

```python
forwarded_unique = np.unique(forwarded,axis=0)
```

```python
assert sum(forwarded[:,2]) == 942 # this matches reported total fees reported below
assert sum(forwarded[:,0]) == 2182528 # this matches total in below
assert sum(forwarded[:,1]) == 2181583 # this matches total out below
# reproducing issue
assert (sum(forwarded[:,0]) - sum(forwarded[:,1])) > sum(forwarded[:,2])
```

```python
len(forwarded_unique), len(forwarded)
```

```python
assert (sum(forwarded_unique[:,0]) - sum(forwarded_unique[:,1])) > sum(forwarded_unique[:,2])
```

```python
sum(forwarded_unique[:,0]) - sum(forwarded_unique[:,1])
```

```python
sum(forwarded_unique[:,0])
```

my reported balances:
```console
total fees: S942
total out: S2,181,583
total in: S2,182,528

total in - total out = S945 (3 sats greater than fees reported)
From(forwarding history -> fees earned page: S941 (4 sats less than in - out)
```

from lnorb reported issue #87:

```console
total fees: 5422225
total in: 6082929908
total out: 6077506166
total out - total in = 5423742 (1517 greater than total fees above)
```

Unable to connect to playground. Could be local connection (coffee shop)

```console
 Traceback (most recent call last):
   File "/Users/asherp/git/orb/orb/orb/misc/channels.py", line 56, in get
     for c in self.lnd.get_channels():
   File "/Users/asherp/git/orb/orb/orb/lnd/lnd_grpc.py", line 127, in get_channels
     ln.ListChannelsRequest(active_only=active_only)
   File "/Users/asherp/opt/miniconda3/envs/orb/lib/python3.7/site-packages/grpc/_channel.py", line 946, in __call__
     return _end_unary_response_blocking(state, call, False, None)
   File "/Users/asherp/opt/miniconda3/envs/orb/lib/python3.7/site-packages/grpc/_channel.py", line 849, in _end_unary_response_blocking
     raise _InactiveRpcError(state)
 grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with:
 	status = StatusCode.UNAVAILABLE
 	details = "failed to connect to all addresses"
 	debug_error_string = "{"created":"@1642885835.275691000","description":"Failed to pick subchannel","file":"src/core/ext/filters/client_channel/client_channel.cc","file_line":3135,"referenced_errors":[{"created":"@1642885835.275690000","description":"failed to connect to all addresses","file":"src/core/lib/transport/error_utils.cc","file_line":163,"grpc_status":14}]}"
 >

```

* ignoring hourly config

To configure for hourly's git based time tracking, add the following `hourly.yaml`

```yaml
work_log:
  header_depth: 3
  filename: worklogs/<your name>.md

repo:
  branch:
  - main
  # list any branches you want to track
```

### 2022-01-22 15:01:03.682659: clock-in

