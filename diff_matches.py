#!/usr/bin/python

# Get difference in matches in 2 results files (generated by search spider, output type 2)
# Output product to be matched, then result in the first file, then result in the second

import sys

lines1 = {}
lines2 = {}


with open(sys.argv[1], "r") as file1:
    with open(sys.argv[2], "r") as file2:
        for line in file1:
            match = line.strip().split(",")
            if len(match) == 1:
                lines1[match[0]] = ""
            else:
                lines1[match[0]] = match[1]
        for line in file2:
            match = line.strip().split(",")
            if len(match) == 1:
                lines2[match[0]] = ""
            else:
                lines2[match[0]] = match[1]

for product in lines1:
    # in case they don't contain the same origin products (for ex for partial results files)
    if product in lines2:
        if lines1[product] != lines2[product]:
            print ",".join([product, lines1[product], lines2[product]])

