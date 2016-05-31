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
from requests import put
from requests.exceptions import RequestException, SSLError

logger = logging.getLogger("zvmExporter")


class Requester:
    """Requester class that makes xCAT API requests.

    :param zhcpnode: Name of the zHCP node. It is used when sending the SMAPI
                     request.
    :param username: Username for xCAT request.
    :param password: Password for xCAT request.
    :param xcat_addr: xCAT server address.
    :param xcat_port: Port to connect to the xCAT server, e.g. 443 for HTTPS
                      (default).
    :type zhcpnode: string
    :type username: string
    :type password: string
    :type xcat_addr: string
    :type xcat_port: int

    """
    def __init__(self, zhcpnode, username, password, xcat_addr, xcat_port=443,
                 cert=None):
        self.xcat_addr = xcat_addr
        self.xcat_port = xcat_port
        self.zhcpnode = zhcpnode
        self.username = username
        self.password = password
        self.cert = cert

    def send_request(self, query_name):
        """Send request via xCAT.

        :param query_name: xCAT query string.
        :type query_name: string

        :returns: query response, or an empty string when the request has
                  failed.
        :rtype: string

        :note: For more information on xCAT queries, refer to the chapter
               Application Programming of the z/VM manual.

        """
        result = ""

        # Prepare HTTP request
        url = ("https://{}:{}/xcatws/nodes/{}/dsh?userName={}&password={}&"
               "format=json").format(self.xcat_addr, self.xcat_port,
                                     self.zhcpnode, self.username,
                                     self.password)
        body = '["command=smcli {}"]'.format(query_name)
        headers = {'content-type': 'text/plain', 'content-length': len(body)}

        logger.info("Sending a request to xCAT...")
        try:
            response = put(url, data=body, headers=headers, timeout=300,
                           verify=False if not self.cert else self.cert)
        except SSLError:
            logger.exception("Problem with SSL verification")
        except RequestException:
            logger.exception("Failed to send the request")
        else:
            result = response.text
            logger.info("Response status: {} {}".format(response.status_code,
                                                        response.reason))

        return result

    def query_page_info(self):
        """Calls :func:`send_request` function with the following query
        ::

            System_Page_Utilization_Query -T ZHCP
        """
        return self.send_request("System_Page_Utilization_Query -T ZHCP")

    def query_spool_info(self):
        """Calls :func:`send_request` function with the following query
        ::

            System_Spool_Utilization_Query -T ZHCP
        """
        return self.send_request("System_Spool_Utilization_Query -T ZHCP")

    def query_cpu_memory_info(self):
        """Calls :func:`send_request` function with the following query
        ::

            System_Performance_Information_Query -T ZHCP -k
            DETAILED_CPU=SHOW=NO
        """
        return self.send_request("System_Performance_Information_Query -T "
                                 "ZHCP -k DETAILED_CPU=SHOW=NO")

    def query_disk_def(self):
        """Calls :func:`send_request` function with the following query
        ::

            Image_Volume_Space_Query_DM -T ZHCP -q 1 -e 1
        """
        # -q 1: query_type DEFINITION - Query volume definition for the
        #       specified image device
        # -e 1: entry_type VOLUME - Query specified volume
        return self.send_request("Image_Volume_Space_Query_DM -T ZHCP -q 1 "
                                 "-e 1")

    def query_disk_free(self):
        """Calls :func:`send_request` function with the following query:
        ::

            Image_Volume_Space_Query_DM -T ZHCP -q 2 -e 1
        """
        # -q 2: query_type FREE - Query amount of free space available on
        #       the specified image
        # -e 1: entry_type VOLUME - Query specified volume
        return self.send_request("Image_Volume_Space_Query_DM -T ZHCP -q 2 "
                                 "-e 1")
