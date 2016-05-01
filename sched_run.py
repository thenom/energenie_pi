#!/usr/bin/env python

import sys, urllib2, time

if len(sys.argv) < 3:
    print 'Please supply an interval in seconds and the ip\hostname!'
    print 'e.g. $ python sched_run.py 5 127.0.0.1'
    sys.exit(1)

wait_time = sys.argv[1]
url = 'http://' + sys.argv[2] + ':8000/powersocket/sched_check'
print 'Running with a delay of ' + str(wait_time) + '...'
print 'Set URL: ' + url

while True:
    try:
        time.sleep(float(wait_time))
        response=urllib2.urlopen(url)
        print response.read()
    except urllib2.URLError as e:
        print e
        print 'Could not connect to the URL, please check that it is running!'
