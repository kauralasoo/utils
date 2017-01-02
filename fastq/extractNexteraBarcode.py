import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Extract Nextera barcode from the fastq file.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--fastq", help = "Path to the fastq file.")
args = parser.parse_args()

#Construct a command
command = " ".join(["zcat ", args.fastq, " | grep CTGTCTCTTATACACATCTCCGAGCCCACGAGAC",
	" | sed 's/$/XXXXXXXXXXXX/g;s/[ATGCNatgcn]*CTGTCTCTTATACACATCTCCGAGCCCACGAGAC//g'",
	" | cut -c 1-8 | grep -v X | sort | uniq -c | sort -n | tail -n 1"])

#Run and report results to STDOUT
subprocess.call(['bash','-c',header_command])
