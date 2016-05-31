# zvm-exporter 

z/VM metrics exporter for [Prometheus](https://github.com/prometheus/prometheus), written in Python.

## Installation

    pip install .

## Running

    zvm_exporter --server <xcat-server-address> --username <xcat-user> --password <xcat-password> --zhcpnode <zhcp-node> -f zvm_exporter.log

## Options

| Name                    | Description                                                                       | Required |
| ----------------------- | --------------------------------------------------------------------------------- | -------- |
| -f FILE, --logfile FILE | specifies the output log file. (defaults to /var/log/prometheus/zvm_exporter.log) | No       |
| --port PORT             | Port on which to expose metrics. (defaults to 9110)                               | No       |
| --zhcpnode NODENAME     | Name of the zHCP node.                                                            | Yes      |
| --username USERNAME     | Username to connect to xCAT with.                                                 | Yes      |
| --password PASSWORD     | Password to connect to xCAT with.                                                 | Yes      |
| --server ADDRESS        | Address to the xCAT server. (port defaults to 443)                                | Yes      |
| -v, --version           | show program's version number and exit                                            | -        |
| -h, --help              | show the help message and exit                                                    | -        |

## List of Metrics

* CPU
* Memory
* Disk
* Paging
* Spool

| System Stats | Metric names                                                        |
| ------------ | ------------------------------------------------------------------- |
| CPU          | zvm\_system\_cpu\_in\_use, zvm\_system\_cpu\_count                  |
| Memory       | zvm\_system\_memory\_in\_use, zvm\_system\_memory\_total            |
| Disk         | zvm\_disk\_status, zvm\_disk\_space\_total, zvm\_disk\_space\_free  |
| Paging       | zvm\_page\_allocated\_total, zvm\_page\_used\_total                 |
| Spool        | zvm\_spool\_allocated\_total, zvm\_spool\_used\_total               |
