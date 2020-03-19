#!/usr/bin/env sh

set -e

ophis -o resources/temp asm/splash.oph
python -c 'import os
d = open("resources/temp", "rb").read()
l = len(d) % 256
if l != 0:
    d += "\x00" * (256 - l)

d += open("resources/TITLE", "rb").read()
open("resources/splash.rom", "wb").write(d)
'
rm resources/temp

rm -f disks/mgc2boot.ssd
tools/dfs_add_files.py indices/mgc2boot.txt disks/mgc2boot.ssd
