import bs4
import argparse
import pathlib
import re

from utils import *


def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='MHTML filename (downloaded from WA)')
    args = parser.parse_args()
    return args


def get_html(filename):
    html_file = pathlib.Path(filename).resolve()
    html = html_file.read_text()
    html = html.replace('=\n', '')
    return html
    

def main():
    args = handle_args()
    html = get_html(args.filename)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    classes = get_classes(soup)


if __name__ == "__main__":
    main()

