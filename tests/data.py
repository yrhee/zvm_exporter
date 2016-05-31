# Dummy response data for testing purposes

page_data = r'{"data":[{"data":["zhcpos2: Total allocated: 93920K\nzhcpos2: ' \
            r'Total used: 33106\nzhcpos2: Available percentage: 1\nzhcpos2: ' \
            r'Volume ID: OSPA35\nzhcpos2: RDEV: ED27\nzhcpos2: Volume total ' \
            r'pages: 2560K\nzhcpos2: Volume pages in use: 834\nzhcpos2: ' \
            r'Available percentage: 1\nzhcpos2: Drain: NOTDRAINED\nzhcpos2: ' \
            r'Drain: NOTDRAINED\nzhcpos2: ERROR: The volume ID of the paging' \
            r' volume is NULL",null]},{"errorcode":["0"]}]}'

spool_data = r'{"data":[{"data":["zhcpos2: \nzhcpos2: Total allocated: ' \
             r'12001K\nzhcpos2: Total used: 4837K\nzhcpos2: Available ' \
             r'percentage: 40\nzhcpos2:   Volume ID: OS263S\nzhcpos2:   ' \
             r'RDEV: 5381\nzhcpos2:   Volume total pages: 1761K\nzhcpos2:   ' \
             r'Volume pages in use: 584468\nzhcpos2:   Available percentage:' \
             r' 32\nzhcpos2:   Dump: NOTDUMP\nzhcpos2:   Drain: NOTDRAINED",' \
             r'null]},{"errorcode":["0"]}]}'

cpu_memory_data = r'{"data":[{"data":["zhcpos2: CPU_COUNT=32\nzhcpos2: ' \
                  r'CPU_AVERAGE_USE=2.125%\nzhcpos2: PAGING_RATE=0\nzhcpos2:' \
                  r' MEMORY_IN_USE=4219345\nzhcpos2: MEMORY_TOTAL=78643200\n' \
                  r'zhcpos2: MONITOR_RATE=2.00 SECONDS \nzhcpos2: ' \
                  r'MONITOR_INTERVAL=1 MINUTES \nzhcpos2: ' \
                  r'MONITOR_EVENT_COUNT=11\nzhcpos2: DOMAIN_MONITOR=ENABLED' \
                  r'\nzhcpos2: DOMAIN_PROCESSOR=DISABLED\nzhcpos2: ' \
                  r'DOMAIN_STORAGE=ENABLED\nzhcpos2: DOMAIN_SCHEDULER=' \
                  r'DISABLED\nzhcpos2: DOMAIN_SEEKS=DISABLED\nzhcpos2: ' \
                  r'DOMAIN_USER=DISABLED\nzhcpos2: DOMAIN_I/O=ENABLED\n' \
                  r'zhcpos2: DOMAIN_NETWORK=ENABLED\nzhcpos2: ' \
                  r'DOMAIN_ISFC=ENABLED\nzhcpos2: DOMAIN_APPLDATA=DISABLED\n' \
                  r'zhcpos2: DOMAIN_SSI=DISABLED",null]},{"errorcode":["0"]}' \
                  r']}'

disk_def_data = r'{"data":[{"data":["zhcpos2: OS2P01 3390-64K 65520 OS2P01\n' \
                r'zhcpos2: OS2P02 3390-64K 65520 OS2P02\nzhcpos2: OS2P03 ' \
                r'3390-64K 65520 OS2P03",null]},{"errorcode":["0"]}]}'

disk_free_data = r'{"data":[{"data":["zhcpos2: $$$$$$ ???? 1 500 * *\n' \
                 r'zhcpos2: $$$$$$ ???? 503 382 * *\nzhcpos2: OS2P01 ' \
                 r'3390-64K 6677 58843 * *\nzhcpos2: OS2P02 ' \
                 r'3390-64K 1 65519 * *"]},{"errorcode":["0"]}]}'

emptyData1 = r'{"data":[{"data":["",null]},{"errorcode":["1"]}]}'

emptyData2 = r'{"data":[{"data":["",""]},{"errorcode":[""]}]}'
