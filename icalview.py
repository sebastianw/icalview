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

    try:
        tzical = tz.tzical(tmpfile)
    except ValueError:
        sys.stderr.write(
            "Sorry, I could not read the calendar file properly.\n" +
            "Please e-mail it to the developer so I can be fixed.\n"
        )
        sys.exit(1)

    try:
        icaltz = tzical.get()
    except ValueError:
        # No Timezone in iCal, assume UTC?
        icaltz = tz.tzutc()

    cal = Calendar.from_ical(cal)
    events = cal.walk('VEVENT')
    evnum = len(events)

    for n, e in enumerate(events):
        if evnum > 1:
            print '** Event %s:' % (n+1)

        # DEBUG
        #print e
        #print "--------"

        start = e['dtstart'].dt.replace(tzinfo=icaltz).astimezone(tz.tzlocal())
        end = e['dtend'].dt.replace(tzinfo=icaltz).astimezone(tz.tzlocal())
        print  'Event: %s' % e['summary'].encode('UTF-8')
        print  'Start: %s' % start.strftime('%a, %Y-%m-%d %H:%M %Z')
        print  'End:   %s' % end.strftime('%a, %Y-%m-%d %H:%M %Z')

        if e.get('organizer'):
            print  'Organizer: %s' % format_atendee(e['organizer'])

        if e.get('status'):
            print  'Status: %s' % e['status']

        if e.get('location'):
            print  'Location: %s' % e['location'].encode('UTF-8')

        if e.get('attendee'):
            print 'Atendee(s):'
            if not isinstance(e['attendee'], basestring):
                for a in e['attendee']:
                    print " %s" % format_atendee(a)
            else:
                print " %s" % format_atendee(e['attendee'])

        if e.get('description'):
            print '\n%s' % e['description'].encode('UTF-8')

if __name__ == "__main__":
    sys.exit(main())
