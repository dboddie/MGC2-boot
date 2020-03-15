#!/usr/bin/env python

import os, sys
import makedfs

if __name__ == "__main__":

    if len(sys.argv) != 3:
        sys.stderr.write("Usage: %s <index file> <SSD file>\n" % sys.argv[0])
        sys.exit(1)
    
    index_file = sys.argv[1]
    ssd_file = sys.argv[2]
    ssd_exists = os.path.exists(ssd_file)
    
    # Read the index file and create a list of files and their new names.
    file_names = []
    
    for line in open(index_file).readlines():
        line = line.strip()
        if not line: break
        if line.startswith("#"): continue
        
        file_name, name, load, exec_ = line.split()
        if "." not in name:
            name = "$." + name
        file_names.append((file_name, name, int(load, 16), int(exec_, 16)))
    
    d = makedfs.Disk()
    if ssd_exists:
        d.open(open(ssd_file, "r+wb"))
    else:
        d.new()
    
    c = d.catalogue()
    title, files = c.read()
    
    for file_name, name, load, exec_ in file_names:
    
        data = open(file_name, "rb").read()
        files.append(makedfs.File(name, data, load, exec_, len(data)))
    
    c.write(title, files)
    
    if not ssd_exists:
        d.file.seek(0, 0)
        open(ssd_file, "wb").write(d.file.read())
    
    sys.exit()
