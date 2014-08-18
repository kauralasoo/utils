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
parser.add_argument("--index", help = "Path to reference index.")
parser.add_argument("--bowtie_args", help = "Additional arguments passed to bowtie.", default = "")
parser.add_argument("--single_end", help = "The reads are single end", default = "False")
parser.add_argument("--suffix", help = "Suffix of the FASTQ files", default = ".fq.gz")

args = parser.parse_args()

for line in fileinput.input("-"):
	line = line.rstrip()
	#specifiy fastq files
	if (args.single_end == "True"):
		fq = os.path.join(args.fastq, line + args.suffix)
		reads_parameter = " ".join(["-U",fq])
	else:
		fq1 = os.path.join(args.fastq, line + ".1" + args.suffix)
		fq2 = os.path.join(args.fastq, line + ".2" + args.suffix)
		reads_parameter = " ".join(["-1", fq1, "-2", fq2])
	sam_file = os.path.join(args.output, line)

	bowtie_command = ' '.join(['bowtie2', "-p", args.ncores, "-x", args.index, reads_parameter ,'| samtools view -F 0xC -bS - | samtools sort -n -m 4000000000 -', sam_file])  
	print(bowtie_command)
	subprocess.call(['bash','-c',bowtie_command])