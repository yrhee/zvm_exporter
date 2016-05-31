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

from setuptools import setup

setup(
    name="zvm_exporter",
    version="1.0.0",
    author="Ye Na Rhee",
    author_email="yrhee@de.ibm.com",
    description=("Prometheus Exporter for z/VM Metrics"),
    packages=["zvm_exporter"],
    package_data={
        "zvm_exporter": [
            "logconf.ini"
        ]
    },
    data_files=[
        ('/var/log/prometheus', [])
    ],
    entry_points={
        "console_scripts": [
            "zvm_exporter = zvm_exporter.__main__:main"
        ]
    },
    install_requires=[
        "prometheus_client>=0.0.13",
        "requests",
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'httpretty'],
    license="MIT",
)
