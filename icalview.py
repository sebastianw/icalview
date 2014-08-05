#! /usr/bin/env python

from icalendar import Calendar
from dateutil import tz
from datetime import datetime
import sys
import StringIO
import re

r_atendee = re.compile(r'mailto:', re.IGNORECASE)
def format_atendee(a):
    return r_atendee.sub('', a)

def main():
    cal = sys.stdin.read()
    tmpfile = StringIO.StringIO()
    tmpfile.write(cal)
    tmpfile.seek(0)
    tzical = tz.tzical(tmpfile)
    try:
        icaltz = tzical.get()
    except ValueError:
        # No Timezone in iCal, assume UTC?
        icaltz = tz.tzutc()
    cal = Calendar.from_ical(cal)
    for e in cal.walk('VEVENT'):
#        print e
#        print "--------"
        start = e['dtstart'].dt.replace(tzinfo=icaltz).astimezone(tz.tzlocal())
        end = e['dtend'].dt.replace(tzinfo=icaltz).astimezone(tz.tzlocal())
        print  'Event: %s' % e['summary'].encode('UTF-8')
        print  'Start: %s' % start.strftime('%a, %Y-%m-%d %H:%M %Z')
        print  'End:   %s' % end.strftime('%a, %Y-%m-%d %H:%M %Z')
        print  'Organizer: %s' % format_atendee(e['organizer'])
        print  'Status: %s' % e['status']
        print  'Location: %s' % e['location'].encode('UTF-8')
        if 'attendee' in e:
            print 'Atendee(s):'
            for a in e['attendee']:
                print " %s" % format_atendee(a)
        print '\n%s' % e['description'].encode('UTF-8')

if __name__ == "__main__":
    sys.exit(main())
