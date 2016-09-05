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
	infile = os.path.join(args.currentDir, sample_id, args.currentSubdir, args.suffix)
	outfile = os.path.join(args.newDir, ".".join([sample_id, args.suffix, args.filename]))

	command = " ".join(["cp", infile, outfile])
	command2 = "gzip " + outfile
	print(command)
	print(command2)

	subprocess.call(['bash','-c',command])
	subprocess.call(['bash','-c',command2])



