# schedule-to-ical

Python program to convert class schedule (Wolverine Access MHTML download) to an iCal file.

### Why?
I'm too lazy to put my classes in my calendar. Why do something that I can make code do for me?

### How?
Python. Beautiful Soup for MHTML parsing, iCalendar for creating the iCal file.

### Learning Goals
- Play with Beautiful Soup (it's awesome)
- Figure out why Wolverine Access and Atlas BOTH don't have a built-in iCal export option (inconclusive).

## Usage
Download an MHTML file from Wolverine Access.

Backpack/Registration > My Class Schedule > List View > Scroll to the bottom and click "Printer friendly page" \
Open Browser Tools and click "Save Page As" > Choose "Webpage, Single File" as format. \

Save somewhere (`src/` directory will do) and specify path to file in command line argument

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
$ python3 src/main.py src/W23ClassSchedule.mht
Generated iCal file W23ClassSchedule.ical
```

### Pitfalls
- Are hardcoded ids and class names the same for everyone? Or the same for the same person for different semesters?

