#!/usr/bin/env sh

set -e

for name in "MMFS.rom"; do
    if [ ! -e resources/$name ]; then
        echo "Ensure that a ready-to-use MMFS.rom file is placed in the resources directory."
        exit 1
    fi
done

ophis -o resources/COPYFN asm/copyrom.oph
python tools/pad_rom.py

cat resources/COPYFN resources/MMFS.rom > resources/COPYROM
rm resources/COPYFN

python tools/make_title.py
python tools/make_rom.py
