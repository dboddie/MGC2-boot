#!/usr/bin/env sh

set -e

ophis -o resources/temp asm/splash.oph
python tools/pad_to_page.py resources/temp

cat resources/temp resources/TITLE > resources/splash.rom
rm resources/temp

rm -f disks/mgc2boot.ssd
tools/dfs_add_files.py indices/mgc2boot.txt disks/mgc2boot.ssd
