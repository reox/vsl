#!/usr/bin/env python3.2

import urllib.request
from html.parser import HTMLParser
from collections import defaultdict
import re


class MyHTMLParser(HTMLParser):
    """
    In this parser we need to implement a litle statemachine, 
    that parses the right stuff from the HTML File 
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
            if 'joint session of 10 meetings' in data:
                if len(data.split('(')) > 2:
                    # there should be another title in front
                    self.title = data.rsplit('(')[-2][:-3].replace('  and ', ', ')
                else:
                    # otherwise take the front stuff
                    self.title = data.split(':', 1)[1].rsplit('(', 1)[0][1:-1]
                    if ':' in self.title:
                        # long Olympic Games title
                        self.title = self.title.split(':', 1)[0]

            else:
                self.title = data.rsplit('(')[-1][:-1].replace('  and ', ', ')

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

    remove_title = ['VSL', 'INFINITY']
    remove_place = ['Naturhistorisches Museum', 'Schönbrunn', 'FH, 2nd floor']
    replace_place = {'FH, Dissertantenraum E104': 'FH, Dissertantenraum'}

    date_matcher = re.compile("[A-Za-z, ]+([0-9]{1,2})[a-z]+")
    all_events = {}
    for k, v in parser.get_result().items():
        date = date_matcher.match(k).group(1) 
        events = defaultdict(list)
        for x, y in v:
            if x not in remove_title and y not in remove_place:
                if y in replace_place:
                    y = replace_place[y]

                # now we need to replace the area and room:
                if ',' in y:
                    building, room = y.split(',')
                    room = room[1:]
                else:
                    building = None
                    room = y
                events[building].append((x, room))
        if len(events) > 0:
            all_events[date] = events

    # all_events contains now a {date-> {building -> [events (name, room)]}}

    room_lookup = {}
    # room lookup is used to look up rooms
    with open("rooms.csv", "r") as f:
        for line in f.readlines():
            building, room, area, floor = line.replace('\n', '').split(',')
            room_lookup[(building, room)] = (area, floor)

    # now generate the signs...
    # generate event signs for FH: 
    print("Generate Event Lists for FH")
    event_list_raw = open("templates/fh_events.tex.tmpl", "r").read()
    for date, events in all_events.items():
        event_list = event_list_raw
        event_list = event_list.replace("$$date$$", date)
        table = "\n".join("%s & %s & %s \\\\" % (event, room_lookup[('FH', room)][0],
            room_lookup[('FH', room)][1]) for event, room in sorted(events['FH']))
        event_list = event_list.replace("$$events$$", table)
        
        with open("../src/freihaus/eventplan/fh_event_%s.tex" % date, "w+") as f:
            f.write(event_list)
            print("\twritten", f.name)

    # generate lift signs
    print("Generate Lift Signs for FH")
    lift_sign_raw = open("templates/fh_lift.tex.tmpl", "r").read()
    for date, events in all_events.items():
        area_signs = defaultdict(lambda: defaultdict(list))
        
        for event, room in events['FH']:
            area, floor = room_lookup[('FH', room)]
            if event not in area_signs[area][floor]: 
                area_signs[area][floor].append(event)

        for area in area_signs.keys():
            workshops = ""
            for floor in range(1,11)[::-1]:
                eventlist = ""
                if floor == 2:
                    eventlist += "\\Coffee{1.5cm} "
                if floor == 1:
                    eventlist += "\\textbf{Registration/Help} "
                    if area != '\\AreaC':
                        eventlist += "(Area \\AreaC) "
                if str(floor) in area_signs[area]:
                    eventlist += ", ".join(sorted(set(area_signs[area][str(floor)])))
                workshops += "\\FN{%d} & %s \\\\\n" % (floor, eventlist)
                if floor != 1:
                    workshops += "\\hline\n"
            sign = lift_sign_raw.replace("$$area$$",
                    area).replace("$$workshops$$", workshops)
            with open("../src/freihaus/lift/fh_lift_%s_%s.tex" %
                    (area.replace('\\', '').lower(), date), "w+") as f:
                f.write(sign)
                print("\twritten", f.name)

    print("generate epsilon signs for FH")
    fh_epsilon_raw = open("templates/fh_epsilon.tex.tmpl", "r").read()
    for date, events in all_events.items():
        for event, room in events['FH']:
            sign = fh_epsilon_raw.replace("$$event$$", event).replace("$$room$$",
            room)
            with open("../src/freihaus/event/event_%s_%s.tex" %
            (event.replace(", ", "").lower(),
                room.replace(" ", "").replace("/", "").lower()), "w+") as f:
                f.write(sign)
                print("\twritten", f.name)

    print("generate epsilon signs for MB")
    fh_epsilon_raw = open("templates/mb_epsilon.tex.tmpl", "r").read()
    for date, events in all_events.items():
        for event, room in events['MB']:
            area, floor = room_lookup[('MB', room)]

            sign = fh_epsilon_raw.replace("$$event$$", event).replace("$$room$$",
            room).replace("$$area$$", area).replace("$$floor$$", floor)
            with open("../src/hauptgebaeude/event/event_%s_%s.tex" %
            (event.replace(", ", "").lower(),
                room.replace(" ", "").replace("/", "").lower()), "w+") as f:
                f.write(sign)
                print("\twritten", f.name)


            
# \FN{floor}
# \Coffee{1.5cm}
# \textbf{Registration/Help} (Area \AreaC)

if __name__ == "__main__":
    main()


