#!/usr/bin/env sh

set -e

ophis -o resources/temp asm/splash.oph
python tools/pad_to_page.py resources/temp

cat resources/temp resources/TITLE > resources/splash.rom
rm resources/temp

ophis -o resources/LROM asm/loadrom.oph
ophis -o resources/LROMS asm/loadroms.oph
ophis -o resources/MROMS asm/mroms.oph

rm -f disks/mgc2boot.ssd
tools/dfs_add_files.py indices/mgc2boot.txt disks/mgc2boot.ssd
