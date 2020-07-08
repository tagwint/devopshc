#!/usr/bin/env python3

import sys
import os
import gzip
import requests


ARGC = len(sys.argv)

YEAR = 2016 if ARGC < 2 else int(sys.argv[1])
print(YEAR)

MONTH = None if ARGC < 3 else int(sys.argv[2])
DAY = None if ARGC < 4 else int(sys.argv[3])
HOUR = None if ARGC < 5 else int(sys.argv[4])

RY = range(YEAR, YEAR + 1)
RM = range(1, 12) if MONTH is None else range(MONTH, MONTH + 1)
RD = range(1, 31) if DAY is None else range(DAY, DAY + 1)
RH = range(0, 23) if HOUR is None else range(HOUR, HOUR + 1)

# tmp file names, reused for every dump file downloaded
GZTMP = 'xtmp.gz'
XTMP = 'xtmp'

TERM = 'Bitcoin'
DOMAIN = 'en'

DUMPRURL = "https://dumps.wikimedia.org/other/pagecounts-raw/"

TOTAL = 0

print("Procesing stastics for term {} in domain {}".format(TERM, DOMAIN))
for y in RY:
    for m in RM:
        for d in RD:
            for h in RH:
                URL = "{}{:04d}/{:04d}-{:02d}/pagecounts-{:04d}{:02d}{:02d}-{:02d}0000.gz".format(DUMPRURL, y, y, m, y, m, d, h)
                print("Getting " + URL + " ... ")
                r = requests.get(URL, allow_redirects=True)
                if r.status_code != 200:
                    print("Failed to get data: {} code:{}".format(URL, r.status_code))
                else:
                    open(GZTMP, 'wb').write(r.content)
                    gzinput = gzip.GzipFile(GZTMP, 'rb')
                    s = gzinput.read()
                    gzinput.close()
                    output = open(XTMP, 'wb')
                    output.write(s)
                    output.close()
                    with open(XTMP, 'r') as f:
                        for line in f:
                            dth = (line.split()[0:3])
                            (domain, term, hits) = (dth)
                            if (domain == DOMAIN) and (term == TERM):
                                print("Hits in {:04d}-{:02d}-{:02d} during the hour:{:02d} - {:5d}".format(y, m, d, h, int(hits)))
                                TOTAL = TOTAL + int(hits)
print("Grand total: {:32d} ".format(TOTAL))
os.unlink(GZTMP)
os.unlink(XTMP)
