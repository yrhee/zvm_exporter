Overview
========

z/VM Exporter
-------------

z/VM Exporter for `Prometheus <http://www.prometheus.io>`_ was developed to enhance the monitoring of z/VM systems. By running the exporter on a machine that can connect to the xCAT management node, the z/VM system metrics can be scraped by the Prometheus monitoring system. 

It makes use of xCAT API request to query the system metrics. The HTTP responses are then parsed to get the information and the metric data is finally wrapped as Prometheus metrics to be exported.


List of Supported Metrics
-------------------------

z/VM Exporter supports the following metrics:

* CPU
* Memory
* Disk
* Paging
* Spool

+-------------+------------------------------------------------------------+
|System Stats |	Metric names                                               |
+=============+============================================================+
|CPU 	      | zvm_system_cpu_in_use, zvm_system_cpu_count                |
+-------------+------------------------------------------------------------+
|Memory       | zvm_system_memory_in_use, zvm_system_memory_total          |
+-------------+------------------------------------------------------------+
|Disk 	      | zvm_disk_status, zvm_disk_space_total, zvm_disk_space_free |
+-------------+------------------------------------------------------------+
|Paging       | zvm_page_allocated_total, zvm_page_used_total              |
+-------------+------------------------------------------------------------+
|Spool 	      | zvm_spool_allocated_total, zvm_spool_used_total            |
+-------------+------------------------------------------------------------+

References
----------

* `z/VM 6.3 Application Programming <http://www.ibm.com/support/knowledgecenter/SSB27U_6.3.0/com.ibm.zvm.v630.zvmappl/zvmappl.htm?cp=SSB27U_6.3.0%2F6>`_
