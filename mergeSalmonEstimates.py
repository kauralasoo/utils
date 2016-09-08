#! /usr/bin/python2.7
import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Merge Salmon estimates from different types of events.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--outputDir", help = "Path to input directory.")
parser.add_argument("--filename", help = "Name of the Salmon output file.")
parser.add_argument("--suffix", help = "Suffix of the new Salmon output file.")
args = parser.parse_args()

for line in fileinput.input("-"):
	sample_id = line.rstrip()
	file1 = os.path.join(args.outputDir, sample_id, ".".join([sample_id, "contained.quant.sf.gz"]))
	file2 = os.path.join(args.outputDir, sample_id, ".".join([sample_id, "upstream.quant.sf.gz"]))
	file3 = os.path.join(args.outputDir, sample_id, ".".join([sample_id, "downstream.quant.sf.gz"]))
	outfile = os.path.join(args.outputDir, sample_id, ".".join([sample_id, "reviseAnnotations.quant.sf.gz"]))

	command = " ".join(["zcat", file1, file2, file3, '| grep -v "^Name" | gzip >', outfile])
	print(command)
	subprocess.call(['bash','-c',command])
