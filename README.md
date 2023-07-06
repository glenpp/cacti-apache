# Apache stats on Cacti (via SNMP)

 	

Following on from the basics of SNMP I did previously, this article now adds my next set of SNMP extension scripts, config, and Cacti templates to monitor an Apache web server.

## Apache Stats

Apache fortunately generates comprehensive stats internally and presents it under the url `http://localhost/server-status?auto` in a form that is easily parsable by scripts. All that is needed is to extract the stats.

Because a number of hits on the server will be needed for each statistic when snmpd is queried, it is a good idea to do some basic caching so that the stats retrieval doesn't become the dominant load on an otherwise lightly loaded server.

The one thing that needs to be changed in Apache's config is to switch to extended stats. On Debian and Ubuntu systems edit the file /etc/apache2/mods-available/status.conf and add the directive "ExtendedStatus on" just before the Location section. Reload apache and it should be ready to go.

## Getting Apache stats over SNMP

As the stats are available to the local machine (localhost or 127.0.0.1) over http, we once again avoid acrobatics discussed previously needed to get some data into snmpd. A single extension script is all that is needed.

To allow caching, I have created an additional directory: /var/local/snmp/cache/

Set this to be owned by snmp so that it can write and modify files in here: chown snmp: /var/local/snmp/cache

There is a choice between a Python script apache\_stats.py and a Shell script apache-stats.sh. The shell script is likely to have more overhead due to spinning up a load of processes each time it gets hit. With Python you will also need the python3-requests package (or at least that's what it's called in Debian / Ubuntu), and with the Shell option you will need wget.

I place this script (make it executable first: chmod +x apache-stats.py) in /etc/snmp

In /etc/snmp/snmpd.conf add the contents of snmpd.conf.cacti-apache or as appropriate if you are using the shell version.

Once you have added all this in you can test apache-stats by running it from the command line with appropriate parameters, and via SNMP by appending the appropriate SNMP OID to the "snmpwalk" commands shown previously.

## Cacti Templates

I have generated some basic Cacti Templates for these Apache stats.

Simply import the template cacti_host_template_apache.xml, and add the graphs you want to the appropriate device graphs in Cacti. It should just work if your SNMP is working correctly for that device (ensure other SNMP parameters are working for that device).
