#!/usr/bin/env sh

set -e

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: `basename $0` <ROM file> <UEF file>"
    exit 1
fi

ophis -o resources/temp asm/bootstrap.oph
cp "$1" resources/temp2
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

UEFtrans.py "$2" new Electron 0
UEFtrans.py "$2" append resources/BOOTSTRAP
