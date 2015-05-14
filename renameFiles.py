#! /usr/bin/python2.7
import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Rename multiple files in a directory.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--samples", help = "Path to a text file that maps old names to new names.")
parser.add_argument("--filedir", help = "Path to dir where all the files are.")
parser.add_argument("--suffix", help = "Suffix of the files to be renamed.")
parser.add_argument("--execute", help = "Execute the script", default = "False")
args = parser.parse_args()

f = open(args.samples)
for line in f:
	line = line.rstrip()
	fields = line.split("\t")
	old_file = os.path.join(args.filedir, fields[0] + args.suffix)
	new_file = os.path.join(args.filedir, fields[1] + args.suffix)
	command = " ".join(["mv", old_file, new_file])
	print(command)
	if args.execute == "True":
		subprocess.call(['bash','-c',command])