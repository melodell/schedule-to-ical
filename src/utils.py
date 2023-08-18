import bs4
import re
import icalendar
import datetime


# Hardcoded patterns for each type of data (from inspecting MHTML page)
CLASS_PATTERN = re.compile('win0divDERIVED_REGFRM1_DESCR20')
TITLE_PATTERN = re.compile('PAGROUPDIVIDER')
LOCATION_PATTERN = re.compile('MTG_LOC')
TIME_PATTERN = re.compile('MTG_SCHED')
DATE_PATTERN = re.compile('MTG_DATES')
SECTION_PATTERN = re.compile('MTG_SECTION')
TYPE_PATTERN = re.compile('MTG_COMP')

day_nums = {"Mo": 0, "Tu": 1, "We": 2, "Th": 3, "Fr": 4, "Sa": 5, "Su": 6}


# Return course name without description (ex. 'EECS485')
def get_class_name(soup):
    title_tag = soup.find('td', attrs={"class": TITLE_PATTERN})
    title = title_tag.contents[0]
    name  = title.partition(' - ')[0]
    return name


# Return class data specified by pattern
# (All data types are formatted the same in the MHTML)
def get_class_data(soup, pattern):
    divs = soup.findAll('div', id=pattern)
    tags = [d.find('span') for d in divs]
    data = [t.contents[0] for t in tags]
    return data


# Reformat time string into list of days and start/end times
def format_times(times):
    days, start_time, end_time = times.replace('-', '').split()
    day_list = [days[i:i+2] for i in range(0, len(days), 2)]
    return day_list, start_time, end_time


# Build a dictionary with class data
# Return a list of sections for the class in class_soup
def build_class(class_soup):
    c = []

    name = get_class_name(class_soup)
    locations = get_class_data(class_soup, LOCATION_PATTERN)
    times = get_class_data(class_soup, TIME_PATTERN)
    dates = get_class_data(class_soup, DATE_PATTERN)
    section_numbers = get_class_data(class_soup, SECTION_PATTERN)
    types = get_class_data(class_soup, TYPE_PATTERN)

    for i in range(len(locations)):
        days, start_time, end_time = format_times(times[i])

        # Error guarding for missing locations or section numbers
        if i >= len(section_numbers):
            section_number = section_numbers[0]
        else:
            section_number = section_numbers[i]

        if i > len(locations):
            location = locations[0]
        else:
            location = locations[i]

        section = {
            "name": name,
            "location": location,
            "days": days,
            "start_time": start_time,
            "end_time": end_time,
            "start_date": dates[i].partition(' - ')[0],
            "end_date": dates[i].partition(' - ')[2],
            "section_number": section_number,
            "type": types[i]
        }
        c.append(section)

    return c


# Return a list of class dictionaries
def get_classes(html):
    soup =  bs4.BeautifulSoup(html, 'html.parser')
    class_divs = soup.findAll('div', id=CLASS_PATTERN)
    classes = []
    for c in class_divs:
        classes.append(build_class(c))
    return classes


# Make datetime from MM/DD/YYYY HH:MM:AM/PM
def get_time(time):
    time = datetime.datetime.strptime(time, '%m/%d/%Y %I:%M%p')
    return time


# Get actual start date for each class section based on day of the week
def get_start_date(start, day):
    dn = day_nums[day]
    start_weekday = start.weekday()
    if start_weekday ==  dn:
        return start
    elif dn > start_weekday:
        diff = dn - start_weekday
        add_days = datetime.timedelta(days=diff)
    else:
        diff = start_weekday - dn
        add_days = datetime.timedelta(days=7-diff)
    return start + add_days


# Return an iCal string with all class events
def make_ical(classes):
    cal = icalendar.Calendar()

    # Some properties are required to be compliant
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')

    for c in classes:
        for section in c:
            name = f'{section["name"]} - {section["type"]}'
            description = f'{section["location"]}\n{section["section_number"]}'

            # Package doesn't support multiday repeats, so make every weekday a separate event
            for day in section['days']:
                event = icalendar.Event()

                start = get_time(section['start_date'] + " " + section['start_time'])
                start_date = get_start_date(start, day)
                end = get_time(datetime.datetime.strftime(start_date, '%m/%d/%Y') + " " + section['end_time'])
                recur = icalendar.vRecur(freq='weekly',
                                         byday=day.upper(),
                                         until=datetime.datetime.strptime(section['end_date'], '%m/%d/%Y') + datetime.timedelta(days=1))

                event.add('summary', name)
                event.add('description', description)
                event.add('dtstart', start_date)
                event.add('dtend', end)
                event.add('rrule', recur)
                cal.add_component(event)

    return cal.to_ical()
