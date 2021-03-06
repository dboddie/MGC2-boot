#!/usr/bin/env sh

set -e

for name in "MMFS.rom"; do
    if [ ! -e resources/$name ]; then
        echo "Ensure that a ready-to-use MMFS.rom file is placed in the resources directory."
        exit 1
    fi
done

ophis -o resources/COPYFN asm/copyrom.oph
python tools/pad_to_page.py resources/COPYFN

# Pad the MMFS ROM.
python tools/pad_rom.py
# Append it to the copyrom binary so it is used as the bootstrap payload.
cat resources/COPYFN resources/MMFS.rom > resources/COPYROM
rm resources/COPYFN

# Make a version of the ROM with MMFS and title screen.
python tools/make_title.py
python tools/make_rom.py

# Make a minimal version of the ROM with MMFS but no title screen.
python tools/make_rom.py --minimal
