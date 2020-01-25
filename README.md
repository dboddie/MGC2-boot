# Mega Games Cartridge 2

This repository contains files and tools for the menu and hardware development
of the Mega Games Cartridge 2 by Retro Hardware.

## Building the Menu ROM

The build process is run from the command line using a shell like `bash` or
possibly `dash`. The process requires Python 2 and the Ophis 6502 assembler.

 * Place the ready-to-use `MMFS` ROM file in the `resources` directory.
 * From the root directory of the repository, run the `build.sh` script.
   This should create a ROM file, `MGC2.rom`, in the repository root.

The ROM should be usable in an emulator or in a real machine.

## Editing the ROM Details

The name, copyright information and version are stored in the
`tools/make_rom.py` script. It should be fairly straightforward to change
these.
