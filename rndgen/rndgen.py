#!/usr/bin/env python3

# Copyright 2020 by the project contributors
# SPDX-License-Identifier: GPL-3.0-only
#
# Author(s): Pavel Benacek <pavel.benacek@gmail.com>

import random
import string

RECORDS=10000
SEL_RECS=500
PREFIX="/home/temp/filelist/"

def writeFile(fileName, seq):
    """
    Write a sequence to the file, each element of the seq is ended with a new line
    """
    with open(fileName,'w') as f:
        for item in seq:
            f.write(item + "\n")


setB=[]
for i in range(RECORDS):
    file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    tmp_path = PREFIX + file_name 
    setB.append(tmp_path)


setA = []
for i in range(SEL_RECS):
    idx = random.randint(0,len(setB)-1)
    temp = setB[idx]
    setB.pop(idx)
    setA.append(temp)

# Save everything to files (diveded by new lines)
writeFile("setA.txt",setA)
writeFile("setB.txt",setB)

print("Done!")
