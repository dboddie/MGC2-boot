#!/usr/bin/env python

import sys

file_name = sys.argv[1]

d = open(file_name, "rb").read()
l = len(d) % 256
if l != 0:
    d += "\x00" * (256 - l)

open(file_name, "wb").write(d)
