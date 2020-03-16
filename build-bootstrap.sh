#!/usr/bin/env sh

set -e

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    echo "Usage: `basename $0` <ROM file> <ROM number> <UEF file>"
    exit 1
fi

python -c 'import sys; n = sys.argv[1];
open("asm/bootstrap-opts.oph", "w").write(
    ".alias rom_number %s\n.alias ram_bank $fcd%i\n" % (n, int(n, 16) & 1))' "$2"

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

UEFtrans.py "$3" new Electron 0
UEFtrans.py "$3" append resources/BOOTSTRAP
