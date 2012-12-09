#!/bin/sh
# Copyright (C) 2012  Glen Pitt-Pladdy
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
# See: http://www.pitt-pladdy.com/blog/_20091114-134615_0000_Apache_stats_on_Cacti_via_SNMP_/

CACHETIME=30
CACHEFILE=/var/local/snmp/cache/apache

# check for cache file newer CACHETIME seconds ago
if [ ! -f $CACHEFILE -o $((`date +%s`-`stat --format=%Y $CACHEFILE`)) -ge $CACHETIME ]; then
	# update the data
	wget --output-document=$CACHEFILE.TMP.$$ --user-agent='SNMP Apache Stats' 'http://localhost/server-status?auto' >/dev/null 2>&1
	mv $CACHEFILE.TMP.$$ $CACHEFILE
fi

# output the data in order (this is because some platforms don't have them all)
for field in \
	'Total Accesses' \
	'Total kBytes' \
	'CPULoad' \
	'Uptime' \
	'ReqPerSec' \
	'BytesPerSec' \
	'BytesPerReq' \
	'BusyWorkers' \
	'IdleWorkers'
do
	if [ "$field" = 'Total kBytes' ]; then
		echo $((`grep "^$field:" <$CACHEFILE | sed "s/^$field: *//"`*1024))
	else
		grep "^$field:" <$CACHEFILE | sed "s/^$field: *//"
	fi
done

# count up the scorecard
scorecard=`grep ^Scoreboard: $CACHEFILE | sed 's/^Scoreboard: *//'`
echo -n $scorecard | sed 's/[^_]//g' | wc -c
echo -n $scorecard | sed 's/[^S]//g' | wc -c
echo -n $scorecard | sed 's/[^R]//g' | wc -c
echo -n $scorecard | sed 's/[^W]//g' | wc -c
echo -n $scorecard | sed 's/[^K]//g' | wc -c
echo -n $scorecard | sed 's/[^D]//g' | wc -c
echo -n $scorecard | sed 's/[^C]//g' | wc -c
echo -n $scorecard | sed 's/[^L]//g' | wc -c
echo -n $scorecard | sed 's/[^G]//g' | wc -c
echo -n $scorecard | sed 's/[^I]//g' | wc -c
echo -n $scorecard | sed 's/[^\.]//g' | wc -c



