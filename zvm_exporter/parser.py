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
import re

logger = logging.getLogger("zvmExporter")


class Parser:
    """Parser class.

    It has only static methods and no constructor method."""
    def __init__(self):
        pass

    @staticmethod
    def make_snake_case(s):
        """Format strings into snake cases.

        :example:
            ::

                >>> make_snake_case('Hello World')
                'hello_world'

        :param s: a string to format
        :type s: string

        :returns: The formatted string
        :rtype: string

        """
        return re.sub('\s', '_', s).lower()

    @staticmethod
    def get_data(response):
        """Helper function to split the data chunk from xCAT response message.

        :param response: xCAT response message.
        :type response: string

        :returns: a list of strings.
        :rtype: list

        """
        # result_rx is regex that matches the following:
        # {"data":[{"data":["..."]},{"errorcode":["..."]}]} or
        # {"data":[{"data":["...","..."]},{"errorcode":["..."]}]}
        result_rx = re.compile(
            r'{"data":\[{"data":\["(?P<data>.+)"(.*)\]},'
            r'{"errorcode":\["(?P<errorcode>.+)"\]}\]}',
            re.DOTALL)

        # use regex to get data out
        result_match = result_rx.match(response)
        if not result_match:
            logger.error("Failed to match response to regex")
            return []
        data = result_match.group('data')
        return data.split('\\n')

    @staticmethod
    def parse_page(zhcpnode, response):
        """Parse function for page query response.

        :param zhcpnode: name of zHCP node.
        :type zhcpnode: string
        :param response: response returned from xCAT query.
        :type response: string

        :returns: a list with a format shown below.
            ::

                {[ "total_allocated": ...,
                    "total_used": ...,
                    "available_percentage": ... }]
        :rtype: list

        """
        host_rx = re.compile(
            r'(?P<host>[^:]+): (?P<field>[^:]+): (?P<value>.+)', re.DOTALL)
        k_rx = re.compile(r'(\d+)K')
        output = {}

        for line in Parser.get_data(response):
            # match regex
            line_match = host_rx.match(line)
            if not line_match:
                continue
            host = line_match.group('host').strip()
            field = line_match.group('field').strip()
            value = line_match.group('value').strip()
            if host != zhcpnode:
                continue
            # ignore data after Volume ID
            elif field == 'Volume ID':
                break
            # get rid of K
            k_match = k_rx.match(value)
            if k_match:
                value = k_match.group(1)
            # convert to int if possible
            try:
                value = int(value)
            except ValueError:
                pass
            # add data to output dictionary
            output[Parser.make_snake_case(field)] = value

        return [output]

    @staticmethod
    def parse_cpu_memory(zhcpnode, response):
        """Parse function for CPU and memory query response.

        :param zhcpnode: name of zHCP node.
        :type zhcpnode: string
        :param response: response returned from xCAT query.
        :type response: string

        :returns: a list with a format shown below.
            ::

                [{ "cpu_count": ...,
                    "cpu_average_use": ...,
                    "memory_in_use": ...,
                    "memory_total": ...,
                }]
        :rtype: list

        """
        host_rx = re.compile(
            r'(?P<host>[^:]+): (?P<field>[^:]+)=(?P<value>.+)', re.DOTALL)
        percent_rx = re.compile(r'([0-9.]+)%')
        output = {}

        for line in Parser.get_data(response):
            # match regex
            line_match = host_rx.match(line)
            if not line_match:
                continue
            host = line_match.group('host').strip()
            field = line_match.group('field').strip()
            value = line_match.group('value').strip()
            if host != zhcpnode:
                continue
            # ignore data after MONITOR_RATE
            elif field == 'MONITOR_RATE':
                break
            # take care of %
            percent_match = percent_rx.match(value)
            if percent_match:
                value = float(percent_match.group(1)) / 100
            try:
                value = float(value)
            except ValueError:
                pass
            # add data to output dictionary
            output[Parser.make_snake_case(field)] = value

        return [output]

    @staticmethod
    def parse_disk(zhcpnode, def_response, free_response):
        """Parse function for disk query response.

        :param zhcpnode: name of zHCP node.
        :type zhcpnode: string
        :param def_response: response returned from xCAT query
                             :func:`requester.query_disk_def`.
        :type def_response: string
        :param free_response: response returned from xCAT query
                              :func:`requester.query_disk_free`.
        :type free_response: string

        :returns: a list with a format shown below.
            ::

                [{
                  "volume": ...,
                  "status": ...,
                  "space_total": ...,
                  "space_free": ...,
                },
                {
                  "volume": ...,
                  "status": ...,
                  "space_total": ...,
                  "space_free": ...,
                }, ...]
        :rtype: list

        """
        def_rx = re.compile(
            r'(?P<host>[^:]+): (?P<volid>\S+) (?P<devtype>\S+) (?P<size>\S+) '
            r'(?P<region_names>.+)')
        free_rx = re.compile(
            r'(?P<host>[^:]+): (?P<volid>.+) (?P<devtype>.+) (?P<start>.+) '
            r'(?P<size>.+) (?P<group_name>.+) (?P<region_name>.+)')
        output = {}

        def_response_data = Parser.get_data(def_response)
        free_response_data = Parser.get_data(free_response)

        # Because we need to have both data to get the final output
        if def_response_data == [] or free_response_data == []:
            return []

        for line in def_response_data:
            # match regex
            line_match = def_rx.match(line)
            if not line_match:
                continue

            volume_dict = {}
            host = line_match.group('host').strip()
            volid = line_match.group('volid').strip()
            size = line_match.group('size').strip()
            if host != zhcpnode:
                continue
            try:
                size = int(size)
            except ValueError:
                pass
            # add data to output dictionary
            volume_dict['volume'] = volid
            volume_dict['space_total'] = size
            volume_dict['status'] = 0
            volume_dict['space_free'] = 0
            output[volid] = volume_dict

        for line in free_response_data:
            # match regex
            line_match = free_rx.match(line)
            if not line_match:
                continue

            host = line_match.group('host').strip()
            volid = line_match.group('volid').strip()
            start = line_match.group('start').strip()
            size = line_match.group('size').strip()
            if host != zhcpnode:
                continue
            try:
                start = int(start)
                size = int(size)
            except ValueError:
                pass
            # add data to output dictionary
            try:
                volume_dict = output[volid]
            except KeyError:
                continue
            if start == 1:
                volume_dict['status'] = 1
            volume_dict['space_free'] += size

        return output.values()
