import argparse
import pathlib

from utils import *


def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='MHTML filename (downloaded from WA)')
    args = parser.parse_args()
    return args


def get_html(filename):
    html_file = pathlib.Path(filename).resolve()
    html = html_file.read_text()
    html = html.replace('=\n', '')  # remove weird line endings
    return html


def write_ical(filename, calendar):
    out_filename = filename.split('.')[0] + '.ics'
    out_file = pathlib.Path(out_filename).resolve()
    with out_file.open('wb') as f:
        f.write(calendar)
    print(f'Generated iCal file {out_filename}')
    

def main():
    args = handle_args()
    html = get_html(args.filename)
    classes = get_classes(html)
    calendar = make_ical(classes)
    write_ical(args.filename, calendar)


if __name__ == "__main__":
    main()

