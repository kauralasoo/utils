#! /usr/bin/python2.7
import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Copy Salmon output files to a new dir and append sample_id.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--currentDir", help = "Path to input directory.")
parser.add_argument("--currentSubdir", help = "Path to input sub-directory.")
parser.add_argument("--newDir", help = "Path to output directory.")
parser.add_argument("--filename", help = "Name of the Salmon output file.")
parser.add_argument("--suffix", help = "Suffix of the new Salmon output file.")
args = parser.parse_args()

for line in fileinput.input("-"):
	sample_id = line.rstrip()
	infile = os.path.join(args.currentDir, sample_id, args.currentSubdir, args.filename)
	outfile = os.path.join(args.newDir, sample_id, ".".join([sample_id, args.suffix, args.filename, "gz"]))

	command = " ".join(["cat", infile, "| gzip >", outfile])
	print(command)
	subprocess.call(['bash','-c',command])



