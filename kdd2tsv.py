import os
import sys
import zlib

"""
- Install pythonnet via: pip install pythonnet
- Download RtfPipe nuget from: https://www.nuget.org/packages/RtfPipe
- Open it as a zip file, copy the dll file from lib > netstandard2.0 and put it right next to this script.
"""
import clr

sys.path.append(os.getcwd())
clr.AddReference("RtfPipe")
from RtfPipe import Rtf, RtfSource
from System.IO import StringReader

"""
Metadata string for Turkish-French (TURFRE_P.KDD) dictionary:
01.01#0#1#01.03.2004#Koral#FONO#@X1#KoralLanguage#TURFRE#TURFRE_P#Sounds#

0: Version
1: Major version?
2: Minor version?
3: Date
4: Creator
5: Publisher
6: ?
7: Lang attribute key?
8: Two ISO 639-2/T or ISO 639-3 Language codes
9: Filename?
10: bool for the existence of sounds files?
"""

HW_SEP = b"\x0D\x00\x0A\x00"
OFFSET = 0x4D5

def rtf2html(raw):
    return Rtf.ToHtml(RtfSource(StringReader(raw)))

def convert(filename):
    hw_list = []
    deflist = []

    f = open(filename, "rb")
    kdd = f.read()[OFFSET:]
    f.close()

    while True:
        try:
            skip = 0
            idx = kdd.index(HW_SEP)
            if kdd[:idx].startswith(b"\x00"):
                skip = 8
            word = kdd[skip:idx].decode("utf-16")
            hw_list.append(word)
            kdd = kdd[idx + 4:]
        except:
            # end of headword section, skip 17 bytes
            kdd = kdd[17:]
            print(f"Found {len(hw_list)} headwords.")
            break    

    j = 0
    while j < len(kdd):
        try:
            if kdd[j] != 0x78:
                j += 1 
                continue
            decomp_obj = zlib.decompressobj()
            decomp = decomp_obj.decompress(kdd[j:])
            decoded = decomp[4:-3].decode()
            if decoded.startswith("{"):
                deflist.append(decoded)
            else:
                deflist.append(decomp[4:].decode())
            j += len(kdd[j:]) - len(decomp_obj.unused_data)
        except zlib.error:
            j += 1
    print(f"Found {len(deflist)} zlib streams.")
    
    basename = os.path.splitext(os.path.basename(filename))[0]
    with open(f"{basename}.tsv", "w", encoding="utf-8") as o:
        o.write(f"Abbreviations\t{rtf2html(deflist[0])}\n")
        for k,v in zip(hw_list, deflist[2:]):
            o.write(f"{k}\t{rtf2html(v)}\n")

    metadata_splt = deflist[1].split("#")
    metadata_kv = {
    "Version"       : metadata_splt[0],
    "Date"          : metadata_splt[3],
    "Creator"       : metadata_splt[4],
    "Publisher"     : metadata_splt[5],
    "From Language" : metadata_splt[8][:3],
    "To Language"   : metadata_splt[8][3:6]
    }

    metadata_lst = [f"{k.ljust(13)} : {v}" for k,v in metadata_kv.items()]
    metadata = "\n".join(metadata_lst)
    with open(f"{basename}_info.txt", "w", encoding="utf-8") as info:
        info.write(metadata)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Missing filename.")
        sys.exit()
    convert(sys.argv[1])