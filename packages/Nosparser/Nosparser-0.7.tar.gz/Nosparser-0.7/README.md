# Drain3

## Introduction

Drain3 is an online log template miner that can extract templates (clusters) from a stream of log messages in a timely
manner. It employs a parse tree with fixed depth to guide the log group search process, which effectively avoids
constructing a very deep and unbalanced tree.

Drain3 continuously learns on-the-fly and automatically extracts "log templates" from raw log entries.

#### Example:

For the input:

```
connected to 10.0.0.1
connected to 10.0.0.2
connected to 10.0.0.3
Hex number 0xDEADBEAF
Hex number 0x10000
user davidoh logged in
user eranr logged in
```

Drain3 extracts the following templates:

```
ID=1     : size=3         : connected to <:IP:>
ID=2     : size=2         : Hex number <:HEX:>
ID=3     : size=2         : user <:*:> logged in
```

Full sample program output:

```
Starting Drain3 template miner
Checking for saved state
Saved state not found
Drain3 started with 'FILE' persistence
reading from std-in (input 'q' to finish)
> connected to 10.0.0.1
Saving state of 1 clusters with 1 messages, 964 bytes, reason: cluster_created (1)
{"change_type": "cluster_created", "cluster_id": 1, "cluster_size": 1, "template_mined": "connected to <:IP:>", "cluster_count": 1}
parameters: ['10.0.0.1']
> connected to 10.0.0.2
{"change_type": "none", "cluster_id": 1, "cluster_size": 2, "template_mined": "connected to <:IP:>", "cluster_count": 1}
parameters: ['10.0.0.2']
> connected to 10.0.0.3
{"change_type": "none", "cluster_id": 1, "cluster_size": 3, "template_mined": "connected to <:IP:>", "cluster_count": 1}
parameters: ['10.0.0.3']
> Hex number 0xDEADBEAF
Saving state of 2 clusters with 4 messages, 1120 bytes, reason: cluster_created (2)
{"change_type": "cluster_created", "cluster_id": 2, "cluster_size": 1, "template_mined": "Hex number <:HEX:>", "cluster_count": 2}
parameters: ['0xDEADBEAF']
> Hex number 0x10000
{"change_type": "none", "cluster_id": 2, "cluster_size": 2, "template_mined": "Hex number <:HEX:>", "cluster_count": 2}
parameters: ['0x10000']
> user davidoh logged in
Saving state of 3 clusters with 6 messages, 1164 bytes, reason: cluster_created (3)
{"change_type": "cluster_created", "cluster_id": 3, "cluster_size": 1, "template_mined": "user davidoh logged in", "cluster_count": 3}
parameters: []
> user eranr logged in
Saving state of 3 clusters with 7 messages, 1168 bytes, reason: cluster_template_changed (3)
{"change_type": "cluster_template_changed", "cluster_id": 3, "cluster_size": 2, "template_mined": "user <:*:> logged in", "cluster_count": 3}
parameters: ['eranr']
q
Clusters:
ID=1     : size=3         : connected to <:IP:>
ID=2     : size=2         : Hex number <:HEX:>
ID=3     : size=2         : user <:*:> logged in
```

This project is an upgrade of the original [Drain](https://github.com/logpai/logparser/blob/master/logparser/Drain)
project by LogPAI from Python 2.7 to Python 3.6 or later with some bug-fixes and additional features.

Read more information about Drain from the following paper:

- Pinjia He, Jieming Zhu, Zibin Zheng, and Michael R.
  Lyu. [Drain: An Online Log Parsing Approach with Fixed Depth Tree](https://pinjiahe.github.io/papers/ICWS17.pdf),
  Proceedings of the 24th International Conference on Web Services (ICWS), 2017.


