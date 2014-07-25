#! /usr/bin/python2.7
# Bowtie alignemt script for mmseq
import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Align RNA-Seq reads to the reference transcriptome using Bowtie.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--fastq", help = "Path to FASTQ folder.")
parser.add_argument("--output", help = "Path to output folder.")
parser.add_argument("--ncores", help = "Number of cores to use.", default = "1")
parser.add_argument("--index", help = "Path to transcriptome index.")
parser.add_argument("--bowtie_args", help = "Additional arguments passed to bowtie.", default = "")
args = parser.parse_args()

for line in fileinput.input("-"):
	line = line.rstrip()
	#specifiy fastq files
	fq1 = os.path.join(args.fastq, line + ".1.fq.gz")
	fq2 = os.path.join(args.fastq, line + ".2.fq.gz")
	sam_file = os.path.join(args.output, line)

	bowtie_command = ' '.join(['bowtie2', "-p", args.ncores, "-x", args.index, "-1", fq1, "-2", fq2 ,'| samtools view -F 0xC -bS - | samtools sort -n -m 4000000000 -', sam_file])  
	print(bowtie_command)
	subprocess.call(['bash','-c',bowtie_command])