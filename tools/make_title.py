#!/usr/bin/env python

"""
Copyright (C) 2020 David Boddie <david@boddie.org.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys
from palette import get_entries, black, red, green, yellow, blue, magenta, \
                    cyan, white
from images import read_png, read_sprite

palette = {"\x00\x00\x00": 0,
           "\xff\x00\x00": 1,
           "\xff\xff\x00": 2,
           "\xff\xff\xff": 3}

rainbow_colours = [red, yellow, green, cyan, blue, magenta]

def rainbow(i, colours, s):

    # Each physical colour is used in two adjacent rows.
    c1 = colours[(i/s) % len(colours)]
    c2 = colours[(((i+1)/s) + 1) % len(colours)]
    return [black, c1, c2, white]

def format_data(data):

    s = ""
    i = 0
    while i < len(data):
        s += ".byte " + ",".join(map(lambda c: "$%02x" % ord(c), data[i:i+24])) + "\n"
        i += 24
    
    return s

def mgc_palette(full = True):

    # Special MGC title palette processing
    
    fe08_data = []
    fe09_data = []
    
    blank = get_entries(4, [black, black, black, black])
    standard = get_entries(4, [black, red, yellow, white])
    
    if full:
        s1, s2 = 111, 65
    else:
        s1, s2 = 43, 3
    
    for i in range(256):
    
        if i >= 128 + s1:
            fe08, fe09 = get_entries(4, rainbow(i - 239, [yellow, cyan, white, green, cyan], 3))
        elif i >= 128 + s2:
            fe08, fe09 = get_entries(4, rainbow(i, rainbow_colours, 3))
        elif full and i >= 128 + 46:
            fe08, fe09 = get_entries(4, rainbow(i, [white, cyan, green, yellow], 3))
        elif full and i > 128:
            fe08, fe09 = get_entries(4, [black, blue, cyan, white])
        else:
            fe08, fe09 = standard
        
        fe08_data.append(fe08)
        fe09_data.append(fe09)
    
    return fe08_data, fe09_data


if __name__ == "__main__":

    if len(sys.argv) != 1:
    
        sys.stderr.write("Usage: %s\n" % sys.argv[0])
        sys.exit(1)
    
    # Convert the PNG to screen data and compress it with the palette data.
    fe08_data, fe09_data = mgc_palette(full = True)
    data, entries = read_png("images/mgc2title.png", palette)
    mgctitle_sprite = read_sprite(data, entries)
    
    # Write the uncompressed title data to a file for other tools to use.
    open("resources/TITLE", "wb").write("".join(map(chr, fe08_data + fe09_data)) + mgctitle_sprite)

    # Create .inf files in case the files are missing those.
    open("resources/TITLE.inf", "w").write("$.TITLE 2e00 2e00 %x" % len(open("resources/TITLE").read()))
