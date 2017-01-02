import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Extract Nextera barcode from the fastq file.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--fastq", help = "Path to the fastq file.")
parser.add_argument("--type", help = "Either read1 or read2.")
args = parser.parse_args()

#Construct a command
if args.type == "read1":
	command = " ".join(["zcat ", args.fastq, " | grep CTGTCTCTTATACACATCTCCGAGCCCACGAGAC",
		" | sed 's/$/XXXXXXXXXXXX/g;s/[ATGCNatgcn]*CTGTCTCTTATACACATCTCCGAGCCCACGAGAC//g'",
		" | cut -c 1-8 | grep -v X | sort | uniq -c | sort -n | tail -n 1 | awk '{print $2}'"])
else if args.type == "read2":
	command = " ".join(["zcat ", args.fastq, " | grep CTGTCTCTTATACACATCTGACGCTGCCGACGA",
		" | sed 's/$/XXXXXXXXXXXX/g;s/[ATGCNatgcn]*CTGTCTCTTATACACATCTGACGCTGCCGACGA//g'",
		" | cut -c 1-8 | grep -v X | sort | uniq -c | sort -n | tail -n 1 | awk '{print $2}'"])
else:
	error("Unknown read type specified.")

#Run and report results to STDOUT
subprocess.call(['bash','-c',command])
