#!/usr/bin/env sh

set -e

ophis -o resources/temp asm/bootstrap.oph
#cp resources/MGCSRMN.rom resources/temp2
cp resources/MMFS.rom resources/temp2
python -c '
import os
padding = 16384 - os.stat("resources/temp2").st_size
open("resources/temp2", "ab").write("\x00"*padding)
'
cat resources/temp resources/temp2 > resources/BOOTSTRAP
rm resources/temp resources/temp2

python -c '
open("resources/BOOTSTRAP.inf", "w").write("$.BOOTSTRAP 1000 1000 %x" % len(open("resources/BOOTSTRAP").read()))
'

UEFtrans.py BOOT.uef new Electron 0
UEFtrans.py BOOT.uef append resources/BOOTSTRAP
