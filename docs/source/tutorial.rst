Getting Started
===============

Installation
------------

To install zvm_exporter package, clone the repository and install using ``pip``::

    $ cd zvm-exporter
    $ pip install .

Running
-------

zvm_exporter can be easily run with::

    zvm_exporter --server <xcat-server-address> --username <xcat-user> --password <xcat-password> --zhcpnode <zhcp-node> -f zvm_exporter.log

With the exporter running, we can now access the metrics at ``http://localhost:9110/metrics``. The port number can be changed with the command line argument ``--port``.

Available options are:

+-------------------------+-----------------------------------------------------------------------------------+------------+
| Name                    | Description                                                                       | Required   |
+=========================+===================================================================================+============+
| -f FILE, --logfile FILE | specifies the output log file. (defaults to /var/log/prometheus/zvm_exporter.log) | No         |
+-------------------------+-----------------------------------------------------------------------------------+------------+
|--port PORT              | Port on which to expose metrics. (defaults to 9110)                               | No         |
+-------------------------+-----------------------------------------------------------------------------------+------------+
|--zhcpnode NODENAME      | Name of the zHCP node.                                                            | Yes        |
+-------------------------+-----------------------------------------------------------------------------------+------------+
|--username USERNAME      | Username to connect to xCAT with.                                                 | Yes        |
+-------------------------+-----------------------------------------------------------------------------------+------------+
|--password PASSWORD      | Password to connect to xCAT with.                                                 | Yes        |
+-------------------------+-----------------------------------------------------------------------------------+------------+
|--server ADDRESS         | Address to the xCAT server. (port defaults to 443)                                | Yes        |
+-------------------------+-----------------------------------------------------------------------------------+------------+
|-v, --version            |show program's version number and exit                                             | -          |
+-------------------------+-----------------------------------------------------------------------------------+------------+
|-h, --help               | show the help message and exit                                                    | -          |
+-------------------------+-----------------------------------------------------------------------------------+------------+

Grafana Dashboard
-----------------

`Grafana <http://www.grafana.org>`_ GUI can be used to visualize metrics collected by Prometheus. There is an example grafana dashboard for z/VM metrics that you can start with. 

Grafana has to be installed and running before following the steps below.

You then need ``grafyaml`` from the openstack-infra project. Get the latest version from the GitHub and install it::

    $ git clone https://github.com/openstack-infra/grafyaml
    $ cd grafyaml
    $ pip install .

Load the example dashboard from the YAML file provided (``grafana_dashboard.yaml``) in your Grafana::

    $ grafana-dashboard update grafana_dashboard.yaml
