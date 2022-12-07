import bs4
import re


# Hardcoded patterns for each type of data (from inspecting MHTML page)
CLASS_PATTERN = re.compile('win0divDERIVED_REGFRM1_DESCR20')
TITLE_PATTERN = re.compile('PAGROUPDIVIDER')
LOCATION_PATTERN = re.compile('MTG_LOC')
TIME_PATTERN = re.compile('MTG_SCHED')
DATE_PATTERN = re.compile('MTG_DATES')
SECTION_PATTERN = re.compile('MTG_SECTION')
TYPE_PATTERN = re.compile('MTG_COMP')


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
        section = {
            "name": name,
            "location": locations[i],
            "time": times[i],
            "dates": dates[i],
            "section_number": section_numbers[i],
            "type": types[i]
        }
        c.append(section)
        
    return c


# Return a list of class dictionaries
def get_classes(soup):
    class_divs = soup.findAll('div', id=CLASS_PATTERN)
    classes = []
    for c in class_divs:
        classes.append(build_class(c))
    return classes
