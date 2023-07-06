#!/usr/bin/env python3
# Copyright (C) 2009-2018  Glen Pitt-Pladdy
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#
# See: https://www.pitt-pladdy.com/blog/_20091114-134615_0000_Apache_stats_on_Cacti_via_SNMP_/

import os
import time
import requests


CACHETIME = 30
CACHEFILE = '/var/local/snmp/cache/apache'
HOST = 'localhost'

# check for cache file newer CACHETIME seconds ago
if os.path.isfile(CACHEFILE) and (time.time() - os.stat(CACHEFILE )[8]) < CACHETIME:
    # use cached data
    f = open(CACHEFILE, 'rt')
    data = f.read()
    f.close()
else:
    # grab the status URL (fresh data)
    # need debian package python-urlgrabber
    r = requests.get('http://{}/server-status?auto'.format(HOST), headers={'User-Agent': 'SNMP Apache Stats'})
    if r.status_code != 200:
        raise Exception("Bad http code: {}".format(r.status_code))
    data = r.text
    # write file
    tmpfile = '{}.TMP.{}'.format(CACHEFILE, os.getpid())
    f = open(tmpfile, 'wt')
    f.write(data)
    f.close()
    os.rename(tmpfile, CACHEFILE )


# dice up the data
scoreboardkey = [ '_', 'S', 'R', 'W', 'K', 'D', 'C', 'L', 'G', 'I', '.' ]
params = {}
section = 'status'
for line in data.splitlines():
    # first line might be the hostname
    if line == HOST:
        section = 'status'
        continue
    elif line == 'TLSSessionCacheStatus':
        section = line
        continue
    # else split field: value pair
    fields = line.split( ': ' )
    # process according to section
    if section == 'status':
        if fields[0] == 'Scoreboard':
            # count up the scoreboard into states
            states = {}
            for state in scoreboardkey:
                    states[state] = 0
            for state in fields[1]:
                states[state] += 1
        elif fields[0] == 'Total kBytes':
            # turn into base (byte) value
            params[fields[0]] = int(fields[1])*1024
        else:
            # just store everything else
            params[fields[0]] = fields[1]
    elif section == 'TLSSessionCacheStatus':
        pass    # TODO

# output the data in order (this is because some platforms don't have them all)
dataorder = [
    'Total Accesses',
    'Total kBytes',
    'CPULoad',
    'Uptime',
    'ReqPerSec',
    'BytesPerSec',
    'BytesPerReq',
    'BusyWorkers',
    'IdleWorkers'
]
for param in dataorder:
    try:
        print(params[param])
    except:    # not all Apache's have all stats
        print('U')

# print the scoreboard
for state in scoreboardkey:
    print(states[state])

