#!/usr/bin/env python

data = open("resources/MMFS.rom", "rb").read()
if len(data) < 16384:
    data += b"\x00" * (16384 - len(data))

open("resources/MMFS.rom", "wb").write(data)
