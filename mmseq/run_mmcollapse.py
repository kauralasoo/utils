#! /usr/bin/python2.7
import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Collapse transcripts to non-redundant transcript sets.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--output", help = "Path to output folder.")
parser.add_argument("--ncores", help = "Number of cores to use.", default = "1")
args = parser.parse_args()

basenames = list()
for line in fileinput.input("-"):
	line = line.rstrip()
	out_base = os.path.join(args.output, line)
	basenames.append(out_base)

basenames = " ".join(basenames)
command = " ".join(["OMP_NUM_THREADS=" + args.ncores,"mmcollapse", basenames])
print(command)
subprocess.call(['bash','-c',command])