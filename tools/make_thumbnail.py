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
import Image
from palette import get_entries, black, red, green, yellow, blue, magenta, \
                    cyan, white
from images import read_image, read_sprite
from distance_pair import compress

palette = {"\x00\x00\x00": 0,
           "\xff\x00\x00": 1,
           "\x00\xff\x00": 2,
           "\xff\xff\x00": 3,
           "\x00\x00\xff": 4,
           "\xff\x00\xff": 5,
           "\x00\xff\xff": 6,
           "\xff\xff\xff": 7}

def compress_best(data):

    compression_results = []
    
    for compress_offset_bits in range(3, 8):
    
        cdata = "".join(map(chr, compress(data,
            offset_bits = compress_offset_bits)))
        
        l = len(cdata)
        if compression_results and l > compression_results[0][0]:
            break
        
        compression_results.append((l, cdata, compress_offset_bits))
    
    compression_results.sort()
    cdata, compress_offset_bits = compression_results[0][1:]
    print "Compressed from %i to %i bytes with %i-bit offset." % (
        len(data), len(cdata), compress_offset_bits)
    
    offset_mask = (1 << compress_offset_bits) - 1
    count_mask = 0xff ^ offset_mask
    
    return chr(count_mask) + chr(compress_offset_bits) + cdata


if __name__ == "__main__":

    if len(sys.argv) != 4:
        sys.stderr.write("Usage: %s <thumbnail file> <x>,<y>,<w>,<h> <data file>\n" % sys.argv[0])
        sys.exit(1)
    
    thumbnail_file = sys.argv[1]
    x, y, w, h = map(int, sys.argv[2].split(","))
    data_file = sys.argv[3]
    
    im = Image.open(thumbnail_file).convert("RGB").crop((x, y, x + w, y + h))
    #im = im.resize((240, 192), Image.NONE)
    im2 = Image.new("RGB", (320, 128), 0)
    im2.paste(im, ((320 - w)/2, (128 - h)/2))
    
    png, entries = read_image(im2, palette)
    data = read_sprite(png, entries)
    
    compressed_data = compress_best(map(ord, data))
    
    open(data_file, "wb").write(compressed_data)
