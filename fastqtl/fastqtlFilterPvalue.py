import sys
import os
import argparse
import fileinput
import subprocess
import gzip

parser = argparse.ArgumentParser(description = "Filter fastqtl output file by maximum p-value.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--fastqtl", help = "Path to the fastqtl output file with snp coordinates.")
parser.add_argument("--maxp", help = "Maximum p-value to be reported.", type = float)
args = parser.parse_args()

fastqtl_file = gzip.open(args.fastqtl)
for line in fastqtl_file:
	line = line.rstrip()
	fields = line.split(" ")
	if (float(fields[5]) < args.maxp):
		print(line)
