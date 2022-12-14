# schedule-to-ical

Python program to convert class schedule (Wolverine Access MHTML download) to an iCal file.

### Why?
I'm too lazy to put my classes in my calendar.

### How?
Python. [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) for MHTML parsing, [iCalendar](https://icalendar.readthedocs.io/en/latest/index.html) for creating the iCal file.

### Learning Goals
- Play with Beautiful Soup (it's awesome)
- Understand the iCal (.ics) file structure
- Figure out why Wolverine Access and Atlas BOTH don't have a built-in iCal export option (inconclusive).
- More practice programming in Emacs :)

## Usage
Download an MHTML file from Wolverine Access.

Backpack/Registration > My Class Schedule > List View > Scroll to the bottom and click "Printer friendly page" \
Open Browser Tools and click "Save Page As" > Choose "Webpage, Single File" format. 

Save somewhere and specify path to file in command line argument.

### Virtual Environment
``` console
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

### Generate iCal File from MHTML
``` console
$ which python
/Users/melinaodell/src/personal/schedule-to-ical/env/bin/python
$ python3 src/main.py W23ClassSchedule.mht
Generated iCal file W23ClassSchedule.ics
```

### Pitfalls
- `icalendar` doesn't allow recurrence for one event on multiple days of the week. Each weekday is a separate event. 

