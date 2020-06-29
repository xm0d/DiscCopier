from sys import argv
from hashlib import sha1, md5

if len(argv) != 2 \
        or len(argv[1]) != 2 \
        or argv[1][1] != ":" \
        or not argv[1][0].isalpha():
    print("Użyj: python cd-dvd-checksum.py D:")
    print("Gdzie D: to litera twojego napedu CD/DVD")

vh = open(r"\\.\%s" % argv[1], "rb")