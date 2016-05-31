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
import logging.config
import os
import sys
import argparse
import re
from time import sleep

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from zvm_exporter.collector import ZVMCollector
from zvm_exporter import __version__


def create_parser():
    parser = argparse.ArgumentParser(
        description="zVM Exporter for Prometheus. Metrics are exported to "
                    "localhost.")

    parser.add_argument(
        "-f", "--logfile",
        help="Output log file. If not provided, logs will not be output to "
             "file.")

    parser.add_argument(
        "-p", "--port",
        help="Port on which to expose metrics. (defaults to 9110)",
        type=int,
        default='9110')

    parser.add_argument(
        "--zhcpnode",
        help="Name of the zHCP node.",
        required=True)

    parser.add_argument(
        "--username",
        help="User name to connect to xCAT with.",
        required=True)

    parser.add_argument(
        "--password",
        help="Password to connect to xCAT with.",
        required=True)

    parser.add_argument(
        "--server",
        help="Address to the xCAT server. (port defaults to 443)",
        required=True)

    parser.add_argument(
        "-v", "--version",
        action="version", version="%(prog)s " + __version__)

    parser.add_argument(
        "--cert",
        help="SSL cert file. If not provided, SSL verification is disabled.",
        default=None)

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    # log configuration
    loginipath = os.path.join(os.path.dirname(__file__)) + '/' + "logconf.ini"
    logging.config.fileConfig(
        loginipath,
        defaults={'logfilename': args.logfile}
        )
    logger = logging.getLogger("zvmExporter")

    # split address and port
    addr_rx = re.compile(
        r'(?P<addr>[a-zA-Z0-9][a-zA-Z0-9\-]*(\.[a-zA-Z0-9][a-zA-Z0-9\-]*)+)'
        r'(:(?P<port>\d+))?')
    match = addr_rx.match(args.server)
    if match:
        xcat_addr = match.group('addr')
        xcat_port = match.group('port') or '443'
    else:
        logger.info("Invalid address")
        return 1

    logger.info("Program started")

    # start collector
    REGISTRY.register(ZVMCollector(args.zhcpnode, args.username,
                                   args.password, xcat_addr, xcat_port,
                                   args.cert))
    start_http_server(args.port)
    while True:
        sleep(1)


if __name__ == "__main__":
    sys.exit(main())
