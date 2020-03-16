#!/usr/bin/env python

import os
import makedfs

os.system("ophis -o resources/LROM asm/loadrom.oph")
os.system("ophis -o resources/LROMS asm/loadroms.oph")

d = makedfs.Disk()
d.new()

c = d.catalogue()

import_files = [("$.LROM", "resources/LROM", 0x1000, 0x1000),
                ("$.LROMS", "resources/LROMS", 0x1000, 0x1000)]
files = []

for name, file_name, load, exec_ in import_files:
    data = open(file_name, "rb").read()
    files.append(makedfs.File(name, data, load, exec_, len(data)))

c.write("LROMS", files)
d.file.seek(0, 0)

open("resources/LROMS.ssd", "wb").write(d.file.read())
