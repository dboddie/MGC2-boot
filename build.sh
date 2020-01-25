#!/usr/bin/env sh

set -e

for name in "MMFS.rom"; do
    if [ ! -e resources/$name ]; then
        echo "Ensure that a ready-to-use MMFS.rom file is placed in the resources directory."
        exit 1
    fi
done

# Create .inf files in case the files are missing those.
python -c '
open("resources/TITLE.inf", "w").write("$.TITLE 2e00 2e00 %x" % len(open("resources/TITLE").read()))
'

ophis -o resources/COPYFN asm/copyrom.oph
python tools/pad_rom.py

cat resources/COPYFN resources/MMFS.rom > resources/COPYROM
rm resources/COPYFN

python tools/make_title.py
python tools/make_rom.py
