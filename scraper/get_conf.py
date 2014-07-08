#!/usr/bin/env python3.2

import urllib.request
from html.parser import HTMLParser
from collections import defaultdict


class MyHTMLParser(HTMLParser):
    """
    In this parser we need to implement a litle statemachine, 
    that parses the right 
    """

    def __init__(self):
        super().__init__()
        self.found_content = 0
        self.events = defaultdict(list)

        self.date = ''
        self.title = ''

        self.inheading = False
        self.inroom = False


    def handle_starttag(self, tag, attrs):
        if tag == 'div' and ('class', 'heading') in attrs:
            self.inheading = True

        if tag == 'div' and ('class', 'room') in attrs:
            self.inroom = True

        if tag == 'div' and ('id', 'content') in attrs:
            self.found_content = 1
        elif tag == 'div' and ('class', 'date') in attrs:
            self.found_content = 2
        elif tag == 'span' and ('class', 'title') in attrs:
            self.found_content = 3
        elif tag == 'span' and ('class', 'room_name') in attrs:
            self.found_content = 4


    def handle_endtag(self, tag):
        if self.inheading and tag == 'div':
            self.inheading = False

        if self.inroom and tag == 'div':
            self.inroom = False


    def handle_data(self, data):
        if self.found_content == 2:
        # we found the date
            self.date = data
            self.found_content = 0
        elif self.found_content == 3 and self.inheading:
        # we found the title
            self.title = data.rsplit('(')[-1][:-1]
        elif self.found_content == 4 and self.inroom:
        # we found the room
            room = data
            if not (self.title, room) in self.events[self.date]:
                self.events[self.date].append((self.title, room))


    def get_result(self):
        return self.events



def main():
    url = "http://www.easychair.org/smart-program/VSL2014/program.html"
    response = urllib.request.urlopen(url)
    html = response.read()

    parser = MyHTMLParser()
    parser.feed(html.decode('UTF-8', 'replace'))

    for k, v in parser.get_result().items():
        print(k)
        for x,y in v:
            print('\t', x, '---', y)

    # Need to clean the dataset.
    # Events that are called VSL go out.
    # every room begins with the building code
    # we have some events with 'and'
    # joint session of 10 meetings
    #  EI, EI 7 + EI 9, EI 10 + FH, Hörsaal 1
    #   ARW-DT, VERIFY  and WING


if __name__ == "__main__":
    main()


