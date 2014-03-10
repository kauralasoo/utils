#! /usr/bin/python2.7
import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Map reads to transcript sets using bam2hits.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--output", help = "Path to output folder.")
parser.add_argument("--ncores", help = "Number of cores to use.", default = "1")
args = parser.parse_args()

for line in fileinput.input("-"):
	line = line.rstrip()
	hits_file = os.path.join(args.output, line + ".hits")
	out_base = os.path.join(args.output, line)
	command = " ".join(["OMP_NUM_THREADS=" + args.ncores,"mmseq", hits_file, out_base])
	print(command)
	subprocess.call(['bash','-c',command])