#! /usr/bin/python2.7
# Script to fetch reads from irods and convert them to Fastq
import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Remove BWA header from the BAM file.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Path to input directory.")
parser.add_argument("--outdir", help = "Path to output directory.")
parser.add_argument("--insuffix", help = "Suffix of the input bam file.", default = ".filtered.bam")
parser.add_argument("--outsuffix", help = "Suffix of the output bam file.", default = ".reheadered.bam")
args = parser.parse_args()

for line in fileinput.input("-"):
		sample_name = line.rstrip()
		path_in = os.path.join(args.indir, sample_name, sample_name + args.insuffix)
		header_out = os.path.join(args.outdir, sample_name, sample_name + ".new_header.txt")
		path_out = os.path.join(args.outdir, sample_name, sample_name + args.outsuffix)
		extract_header = " ".join(["samtools view -H", path_in, "| grep -v 'ID:bwa' > ", header_out])
		reheader_command = " ".join(["samtools reheader", header_out, path_in, ">", path_out])
		print(extract_header)
		subprocess.call(['bash','-c',extract_header])
		print(reheader_command)
		subprocess.call(['bash','-c',reheader_command])

