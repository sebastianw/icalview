icalview
========

Python based iCal viewer for iCal events, primarily for displaying iCal events in mutt

To use this in mutt put it somewhere in your path and configure it accordingly:

`~/.mailcap`:

```
text/calendar; icalview.py; copiousoutput
```

`~/.muttrc`:

```
auto_view text/calendar

# Add it to your alternative_order if you already have one
alternative_order text/calendar text/plain text/html
```
