# Synthetic inventor disclosure: clock-aligned sensor records

This fictional disclosure is supplied only for skill evaluation.

A monitoring system has three temperature sensor nodes and a gateway. Every sensor
node samples temperature once per 50 milliseconds and sends a record containing the
measured temperature, its local timestamp, and the node identifier. Every five
seconds, the gateway sends a synchronization message containing the gateway time.

Each node calculates an offset between its local clock and the gateway time and
stores the latest offset. Before transmission, the node subtracts that offset from
the local timestamp. The gateway orders received records using the corrected
timestamps. This reduces ordering errors caused by clock drift between the nodes.

The node controller executes stored instructions for sampling, offset calculation,
timestamp correction, and transmission. Those instructions are stored in flash
memory soldered to the node controller board. The inventors have implemented the
described system but supplied no numerical measurement of the reduction in ordering
errors and no alternative synchronization protocol.
