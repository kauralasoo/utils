#! /usr/bin/python2.7
import os
import sys
import argparse
import fileinput

parser = argparse.ArgumentParser(description = "Move BAMS from tophat2 folders to single folder and rename.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Path to TopHat2 output folder", default = "tophat2")
parser.add_argument("--outdir", help = "Place to store all BAMs.", default = "bams_tophat2")
args = parser.parse_args()

for line in fileinput.input("-"):
	line = line.rstrip()
	bam_in = os.path.join(args.indir, line, "accepted_hits.bam")
	bam_out = os.path.join(args.outdir, line + ".bam")
	command = " ".join(["mv",bam_in, bam_out])
	print(command)
	os.system(command)

	