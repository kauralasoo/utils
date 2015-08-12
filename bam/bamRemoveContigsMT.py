#! /usr/bin/python2.7
# Script to fetch reads from irods and convert them to Fastq
import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Remove reads mapping to contigs and MT chromosome. Keep only properly paired reads.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Path to input directory.")
parser.add_argument("--outdir", help = "Path to output directory.")
parser.add_argument("--insuffix", help = "Suffix of the input bam file.", default = ".sortedByCoord.bam")
parser.add_argument("--outsuffix", help = "Suffix of the output bam file.", default = ".filtered.bam")
args = parser.parse_args()

for line in fileinput.input("-"):
		sample_name = line.rstrip()
		path_in = os.path.join(args.indir, sample_name, sample_name + args.insuffix)
		path_out = os.path.join(args.outdir, sample_name, sample_name + args.outsuffix)
		chr_list = "1 10 11 12 13 14 15 16 17 18 19 2 20 21 22 3 4 5 6 7 8 9 X Y"
		command = " ".join(["samtools view -h -b -f 2", path_in, chr_list, ">", path_out])
		print(command)
		subprocess.call(['bash','-c',command])
