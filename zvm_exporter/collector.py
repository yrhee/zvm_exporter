# The MIT License (MIT)

# Copyright (c) 2016 IBM Corporation

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import logging
from prometheus_client.core import GaugeMetricFamily
from zvm_exporter.requester import Requester
from zvm_exporter.parser import Parser

logger = logging.getLogger("zvmExporter")


class ZVMCollector(object):
    """Prometheus Collector class.

    An instance of this class will be registered in
    prometheus_client.core.REGISTRY.

    :example:
        ::

            from prometheus_client.core import REGISTRY
            REGISTRY.register(ZVMCollector(args.zhcpnode, args.username,
            args.password, xcat_addr, xcat_port))

    :param zhcpnode: Name of the zHCP node. It is used when sending the SMAPI
                     request.
    :param username: Username for xCAT request.
    :param password: Password for xCAT request.
    :param xcat_addr: xCAT server address.
    :param xcat_port: Port to connect to the xCAT server, e.g. 443 for HTTPS.

    """

    def __init__(self, zhcpnode, username, password, xcat_addr, xcat_port,
                 cert=None):
        self.zhcpnode = zhcpnode
        self.requester = Requester(zhcpnode, username, password, xcat_addr,
                                   xcat_port, cert)

    def collect(self):
        """Main collect function.

        :note: Prometheus Collector should have collect function.

        :yields: GaugeMetricFamily objects of prometheus_client.core.

        """

        logger.info("Starting metric collection...")
        page_metrics = self.collect_page()
        spool_metrics = self.collect_spool()
        cpu_memory_metrics = self.collect_cpu_memory()
        disk_metrics = self.collect_disk()

        logger.info("Yielding metrics...")
        for m in page_metrics:
            for v in page_metrics[m].values():
                yield v

        for m in spool_metrics:
            for v in spool_metrics[m].values():
                yield v

        for m in cpu_memory_metrics:
            for v in cpu_memory_metrics[m].values():
                yield v

        for m in disk_metrics:
            for v in disk_metrics[m].values():
                yield v

    def build_metrics(self, metrics_dict, namespace, labels, parse_fn,
                      *query_fn):
        """Helper function for building metrics.

        Send a query, parse the response and return the metrics in an
        appropriate form.

        :param metrics_dict: a dictionary. It should have the following format:
            ::

                metrics_dict = {
                    "key1": (
                        "metric_name1",
                        "metric_description"),
                    "key2": (
                        "metric_name1",
                        "metric_description")
                    }

            where ``key`` is the name of the key in the dictionary returned by
            the parse function,
            ``metric_name`` is the name of the exported metric and
            ``metric_description`` is the description for the metric.

        :param labels: a list of strings that represent the keys for which the
                       value will be added as the metric labels.
        :param parse_fn: Name of the parse function in the :class:`Parser`
                         class.
        :param query_fn: Name(s) of the query function(s) in the
                         :class:`Requester` class.
        :type metrics_dict: dict
        :type labels: list
        :type parse_fn: string
        :type query_fn: string

        :returns: a dictionary with metric names as keys and a dictionary of
                  ``{'value': GaugeMetricFamily}``
        :rtype: dict

        """

        metrics = {}

        if not labels:
            labels = []

        query_result = [getattr(self.requester, f)() for f in query_fn]
        result = getattr(Parser, parse_fn)(self.zhcpnode, *query_result)

        logger.debug("collect_{}: {}".format(namespace, str(result)))

        # If the result is empty
        if result == [{}]:
            return []

        for name, description in metrics_dict.values():
            metric_name = 'zvm_{}_{}'.format(namespace, name)
            metrics[name] = {
                'value': GaugeMetricFamily(
                    metric_name, description, labels=["host"] + labels),
                }

        for item in result:
            for key in metrics_dict:
                name, _ = metrics_dict[key]
                metrics[name]['value'].add_metric(
                    [self.zhcpnode] + [item[x] for x in labels], item[key])

        return metrics

    def collect_page(self):
        """Calls :func:`build_metrics` function for page metrics.

        :returns: a dictionary with metric names as keys and a dictionary of
                  ``{'value': GaugeMetricFamily}`` as corresponding values

                  metric names: zvm_page_allocated_total, zvm_page_used_total
        :rtype: dict

        """

        metrics_dict = {
            "total_allocated": (
                "allocated_total",
                ("The total number of pages allocated for paging use on the "
                 "system")),
            "total_used": (
                "used_total",
                "The total number of pages in use for paging on the system")}

        return self.build_metrics(metrics_dict, "page", [], "parse_page",
                                  "query_page_info")

    def collect_spool(self):
        """Calls :func:`build_metrics` function for spool metrics.

        :returns: a dictionary with metric names as keys and a dictionary of
                  ``{'value': GaugeMetricFamily}`` as corresponding values

                  metric names: zvm_spool_allocated_total,
                  zvm_spool_used_total
        :rtype: dict

        """
        metrics_dict = {
            "total_allocated": (
                "allocated_total",
                ("The total number of pages allocated for spool use on the "
                 "system")),
            "total_used": (
                "used_total",
                "The total number of pages in use for spool on the system")}

        return self.build_metrics(metrics_dict, "spool", [], "parse_page",
                                  "query_spool_info")

    def collect_cpu_memory(self):
        """Calls :func:`build_metrics` function for cpu, memory metrics.

        :returns: a dictionary with metric names as keys and a dictionary of
                  ``{'value': GaugeMetricFamily}`` as corresponding values

                  metric names: zvm_system_cpu_count, zvm_system_cpu_in_use,
                  zvm_system_memory_in_use, zvm_system_memory_total
        :rtype: dict

        """
        metrics_dict = {
            "cpu_count": (
                "cpu_count",
                "The total number of CPU cores"),
            "cpu_average_use": (
                "cpu_in_use",
                "The average amount of CPU used (0.0-1.0)"),
            "memory_in_use": (
                "memory_in_use",
                "Memory in use"),
            "memory_total": (
                "memory_total",
                "Total available memory")}

        return self.build_metrics(metrics_dict, "system", [],
                                  "parse_cpu_memory", "query_cpu_memory_info")

    def collect_disk(self):
        """Calls :func:`build_metrics` function for disk metrics.

        :returns: a dictionary with metric names as keys and a dictionary of
                  ``{'value': GaugeMetricFamily}`` as corresponding values

                  metric names: zvm_disk_status, zvm_disk_space_total,
                  zvm_disk_space_free
        :rtype: dict

        """
        metrics_dict = {
            "status": (
                "status",
                "Usage status of the volume (1: free, 0: used)"),
            "space_total": (
                "space_total",
                "Size of the total disk space defined for the volume"),
            "space_free": (
                "space_free",
                "Size of the free disk space of the volume")}

        return self.build_metrics(metrics_dict, "disk", ["volume"],
                                  "parse_disk", "query_disk_def",
                                  "query_disk_free")
