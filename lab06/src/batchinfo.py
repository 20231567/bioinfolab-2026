#!/usr/bin/env python3
import sys
import glob

if len(sys.argv) < 2:
    print("사용법: python3 batchinfo.py <폴더경로>")
    sys.exit(1)

folder = sys.argv[1]

print("file\tcount")
for path in sorted(glob.glob(folder + "/*.fasta")):
    n = 0
    with open(path) as f:
        for line in f:
            if line.startswith(">"):
                n = n + 1
    print(path + "\t" + str(n))
