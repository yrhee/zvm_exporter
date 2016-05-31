import httpretty
from utils import compare_lists
from zvm_exporter.collector import ZVMCollector
from prometheus_client.core import GaugeMetricFamily
from data import (page_data, spool_data, cpu_memory_data, disk_def_data,
                  disk_free_data)


def request_callback(request, uri, headers):
    """Callback function used by httpretty

    Send a response in place of xCAT.
    """
    data_str = request.body.decode()
    # response based on data
    if data_str == '["command=smcli System_Page_Utilization_Query -T ZHCP"]':
        return 200, headers, page_data
    elif data_str == ('["command=smcli '
                      'System_Spool_Utilization_Query -T ZHCP"]'):
        return 200, headers, spool_data
    elif data_str == ('["command=smcli System_Performance_Information_Query '
                      '-T ZHCP -k DETAILED_CPU=SHOW=NO"]'):
        return 200, headers, cpu_memory_data
    elif data_str == ('["command=smcli Image_Volume_Space_Query_DM -T ZHCP '
                      '-q 1 -e 1"]'):
        return 200, headers, disk_def_data
    elif data_str == ('["command=smcli Image_Volume_Space_Query_DM -T ZHCP '
                      '-q 2 -e 1"]'):
        return 200, headers, disk_free_data
    else:
        assert False


@httpretty.activate
def test_collect_page():
    c = ZVMCollector("zhcpos2", "user", "password", "example.com", 443)
    # HTTP mocker that sends response in place of xCAT
    httpretty.register_uri(
        httpretty.PUT, "http://example.com:443/xcatws/nodes/zhcpos2/dsh",
        body=request_callback, content_type='text/plain')

    metrics = c.collect_page()

    # Make sure it returns the same number of metrics as the size of
    # metrics_list
    assert len(metrics) == 2
    assert compare_lists(metrics.keys(),
                         ["allocated_total", "used_total"])
    # Check that all metrics have the right type
    for metric in metrics:
        assert type(metrics[metric]['value']) == GaugeMetricFamily


@httpretty.activate
def test_collect_spool():
    c = ZVMCollector("zhcpos2", "user", "password", "example.com", 443)
    # HTTP mocker that sends response in place of xCAT
    httpretty.register_uri(
        httpretty.PUT, "http://example.com:443/xcatws/nodes/zhcpos2/dsh",
        body=request_callback, content_type='text/plain')

    metrics = c.collect_spool()

    # Make sure it returns the same number of metrics as the size of
    # metrics_list
    assert len(metrics) == 2
    assert compare_lists(metrics.keys(),
                         ["allocated_total", "used_total"])
    # Check that all metrics have the right type
    for metric in metrics:
        assert type(metrics[metric]['value']) == GaugeMetricFamily


@httpretty.activate
def test_collect_cpu_memory():
    c = ZVMCollector("zhcpos2", "user", "password", "example.com", 443)
    # HTTP mocker that sends response in place of xCAT
    httpretty.register_uri(
        httpretty.PUT, "http://example.com:443/xcatws/nodes/zhcpos2/dsh",
        body=request_callback, content_type='text/plain')

    metrics = c.collect_cpu_memory()

    # Make sure it returns the same number of metrics as the size of
    # metrics_list
    assert len(metrics) == 4
    assert compare_lists(metrics.keys(),
                         ["cpu_count", "cpu_in_use", "memory_in_use",
                         "memory_total"])
    # Check that all metrics have the right type
    for metric in metrics:
        assert type(metrics[metric]['value']) == GaugeMetricFamily


@httpretty.activate
def test_collect_disk():
    c = ZVMCollector("zhcpos2", "user", "password", "example.com", 443)
    # HTTP mocker that sends response in place of xCAT
    httpretty.register_uri(
        httpretty.PUT, "http://example.com:443/xcatws/nodes/zhcpos2/dsh",
        body=request_callback, content_type='text/plain')

    metrics = c.collect_disk()

    # Make sure it returns the same number of metrics as the size of
    # metrics_list
    assert len(metrics) == 3
    assert compare_lists(metrics.keys(),
                         ["status", "space_total", "space_free"])
    # Check that all metrics have the right type
    for metric in metrics:
        assert type(metrics[metric]['value']) == GaugeMetricFamily


@httpretty.activate
def test_collect():
    c = ZVMCollector("zhcpos2", "user", "password", "example.com", 443)
    # HTTP mocker that sends response in place of xCAT
    httpretty.register_uri(
        httpretty.PUT, "http://example.com:443/xcatws/nodes/zhcpos2/dsh",
        body=request_callback, content_type='text/plain')

    # Check that all metrics have the right type
    for value in c.collect():
        assert type(value) == GaugeMetricFamily
