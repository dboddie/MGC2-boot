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

import os, sys
import makedfs

if __name__ == "__main__":

    args = sys.argv[:]
    
    append_files = "-a" in args
    if append_files: args.remove("-a")
    
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: %s [-a] <index file> <SSD file>\n" % sys.argv[0])
        sys.exit(1)
    
    index_file = sys.argv[1]
    ssd_file = sys.argv[2]
    ssd_exists = os.path.exists(ssd_file)
    
    # Read the index file and create a list of files and their new names.
    file_names = []
    boot_option = 0
    title = ""
    
    for line in open(index_file).readlines():
    
        line = line.strip()
        if not line: break
        
        if line.startswith("#"):
            metadata = line.lstrip("#").lstrip()
            if metadata.lower().startswith("title:"):
                title = metadata[6:].lstrip()
            elif metadata.lower().startswith("boot:"):
                text = metadata[5:].lstrip().replace('\\r', '\r')
                file_names.append((None, "$.!BOOT", 0, 0, text))
                boot_option = 3
            continue
        
        pieces = line.split()
        file_name = " ".join(pieces[:-3])
        name, load, exec_ = pieces[-3:]
        load, exec_ = int(load, 16), int(exec_, 16)
        
        if name == "!BOOT":
            if exec_ == 0:
                boot_option = 3
            else:
                boot_option = 1
        
        if "." not in name:
            name = "$." + name
        file_names.append((file_name, name, load, exec_, None))
    
    d = makedfs.Disk()
    if ssd_exists and append_files:
        d.open(open(ssd_file, "r+wb"))
    else:
        d.new()
    
    c = d.catalogue()
    if ssd_exists and append_files:
        old_title, files = c.read()
    else:
        files = []
    
    for file_name, name, load, exec_, data in file_names:
    
        if not data:
            data = open(file_name, "rb").read()
        
        files.append(makedfs.File(name, data, load, exec_, len(data)))
    
    c.boot_option = boot_option
    c.write(title, files)
    
    if not ssd_exists or not append_files:
        d.file.seek(0, 0)
        open(ssd_file, "wb").write(d.file.read())
    
    sys.exit()
