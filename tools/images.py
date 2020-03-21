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

import Image

def read_png(path, palette):

    im = Image.open(path).convert("RGB")
    return read_image(im, palette)

def read_image(im, palette):

    s = im.tostring()
    
    data = []
    entries = set()
    a = 0
    
    i = 0
    while i < im.size[1]:
    
        line = []
        
        j = 0
        while j < im.size[0]:
        
            # Translate RGB values to palette entries.
            value = palette[s[a:a+3]]
            entries.add(value)
            line.append(value)
            a += 3
            j += 1
        
        i += 1
        data.append(line)
    
    return data, sorted(list(entries))

def read_sprite(lines, palette):

    palette = dict([(value, index) for index, value in enumerate(palette)])
    data = ""
    
    # Read 8 rows at a time.
    for row in range(0, len(lines), 8):
    
        width = len(lines[0])
        
        # Read 4 columns at a time.
        for column in range(0, width, 4):
        
            # Read the rows.
            for line in lines[row:row + 8]:
            
                shift = 3
                byte = 0
                for value in line[column:column + 4]:
                
                    pixel = palette[value]
                    if pixel == 1:
                        byte = byte | (0x01 << shift)
                    elif pixel == 2:
                        byte = byte | (0x10 << shift)
                    elif pixel == 3:
                        byte = byte | (0x11 << shift)
                    
                    shift -= 1
                
                data += chr(byte)
    
    return data
