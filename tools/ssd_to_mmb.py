#!/usr/bin/env python

"""
Copyright (C) 2020 David Boddie <david@boddie.org.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os, struct, sys

class MMBError(Exception):
    pass

class MMB:

    Locked = 0
    ReadWrite = 0x0f
    Unformatted = 0xf0
    Invalid = 0xff
    
    def __init__(self):
    
        self.boot_images = [0, 1, 2, 3]
        self.disk_info = []
        self.disks = []
        
        self.f = None
    
    def _str_to_num(self, s):
    
        n = 0
        shift = 0
        for c in s:
            n += ord(c) << shift
            shift += 8
        
        return n
    
    def _safe(self, s):
    
        new = ""
        for c in s:
            if ord(c) < 32:
                break
            new += c
        
        return new
    
    def _status(self, s):
    
        if s == self.Locked:
            return "L"
        elif s == self.ReadWrite:
            return "R/W"
        elif s == self.Unformatted:
            return "U"
        elif s == self.Invalid:
            return "I"
        else:
            return "?"
    
    def open(self, path):
    
        f = open(path, "rb")
        
        # Read the boot image numbers.
        a, b, c, d = f.read(4)
        A, B, C, D = f.read(4)
        self.boot_images = map(self._str_to_num, [a + A, b + B, c + C, d + D])
        
        # Check the next 8 bytes.
        if f.read(8) != ("\x00" * 8):
            raise MMBError("Not an MMB file: %s" % path)
        
        # Read the 511 disk titles and status information.
        self.disk_info = []
        self.disks = []
        
        i = 0
        while i < 511:
            title = f.read(12)
            f.seek(3, 1)
            status = ord(f.read(1))
            self.disk_info.append((title, status))
            self.disks.append((path, 8192 + (i * 204800)))
            i += 1
    
    def show(self, all_images=False):
    
        print "Boot images:"
        for n in self.boot_images:
            print n,
        
        print
        print
        print "Disks:"
        i = 0
        while i < len(self.disks):
        
            title, status = self.disk_info[i]
        
            # Either show all images or those that are locked or read/write.
            if all_images or status in [self.Locked, self.ReadWrite] or i in self.boot_images:
                s = self._safe(title)
                s += " " * (12 - len(s))
                print "%03i %s %s" % (i, s, self._status(status))
            
            i += 1
        
        print
    
    def add(self, path):
    
        f = open(path, "rb")
        title = f.read(8)
        f.seek(0x100, 1)
        title += f.read(4)
        f.close()
        
        if len(self.disk_info) < 511:
            self.disk_info.append((title, 15))
            self.disks.append((path, 0))
        else:
            i = 0
            while i < 511:
            
                t, s = self.disk_info[i]
                
                if s not in [self.Locked, self.ReadWrite]:
                    # Replace images that are not locked or read/write.
                    self.disk_info[i] = (title, 15)
                    self.disks[i] = (path, 0)
                    break
                
                i += 1
    
    def save(self, path):
    
        if os.path.exists(path):
            f = open(path, "r+wb")
        else:
            f = open(path, "wb")
        
        # Write the boot image numbers.
        boot = map(lambda n: n & 0xff, self.boot_images) + \
               map(lambda n: n >> 8, self.boot_images)
        f.write("".join(map(chr, boot)))
        f.write("\x00\x00\x00\x00\x00\x00\x00\x00")
        
        # Write the disk titles and status bytes.
        i = 0
        while i < 511:
        
            if i < len(self.disk_info):
                title, status = self.disk_info[i]
                title += "\x00" * (12 - len(title))
                d = title[:12] + "\x00\x00\x00" + chr(status)
            else:
                d = ("\x00" * 15) + chr(self.Unformatted)
            
            f.write(d)

            i += 1
        
        # Write the disk images.
        i = 0
        while i < min(len(self.disks), 511):
        
            f.seek(8192 + (i * 204800))
            
            # Locate and read the disks referred to.
            ssd_path, offset = self.disks[i]
            
            if ssd_path != path:
                df = open(ssd_path, "rb")
                df.seek(offset)
                f.write(df.read(204800))
                df.close()
            
            i += 1
        
        f.close()


if __name__ == "__main__":

    args = sys.argv[:]
    
    append = "-a" in args
    if append: args.remove("-a")
    
    if len(args) < 2:
        sys.stderr.write("Usage: %s [-a] <MMB file> <SSD file>...\n" % sys.argv[0])
        sys.exit(1)
    
    mmb_file = args[1]
    ssd_files = args[2:]
    
    mmb = MMB()
    
    if os.path.exists(mmb_file) and append:
        try:
            mmb.open(mmb_file)
        except MMBError as exc:
            sys.stderr.write(exc.message + "\n")
            sys.exit(1)
        
        if len(sys.argv) == 2:
            mmb.show()
            sys.exit()
    
    for ssd_file in ssd_files:
        mmb.add(ssd_file)
    
    mmb.save(mmb_file)
