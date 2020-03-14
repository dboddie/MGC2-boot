#!/usr/bin/env python

import os, sys
import makedfs

if __name__ == "__main__":

    if len(sys.argv) < 3:
        sys.stderr.write("Usage: %s <file>... <SSD file>\n" % sys.argv[0])
        sys.exit(1)
    
    file_names = sys.argv[1:-1]
    ssd_file = sys.argv[-1]
    ssd_exists = os.path.exists(ssd_file)
    
    d = makedfs.Disk()
    if ssd_exists:
        d.open(open(ssd_file, "r+wb"))
    else:
        d.new()
    
    c = d.catalogue()
    title, files = c.read()
    
    for file_name in file_names:
    
        name = "$." + os.path.split(file_name)[1][:7]
        data = open(file_name, "rb").read()
        files.append(makedfs.File(name, data, 0x2000, 0x2000, len(data)))
    
    c.write(title, files)
    
    if not ssd_exists:
        d.file.seek(0, 0)
        open(ssd_file, "wb").write(d.file.read())
    
    sys.exit()
