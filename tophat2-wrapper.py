#! /usr/bin/python2.7
import os
import sys
import argparse
import fileinput

parser = argparse.ArgumentParser(description = "Submit multiple Tophat2 alignment jobs to Farm3", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--MEM", help = "Memory requirements for farm (MB).", default = "4500")
parser.add_argument("--out", help = "TopHat2 output folder.", default = "tophat2")
parser.add_argument("--fastq", help = "Path to folder containing FASTQ files", default = "fastq")
parser.add_argument("--ncores", help = "Number of cores to use.", default = "1")
parser.add_argument("--queue", help = "Number of cores to use.", default = "normal")
parser.add_argument("--library", help = "library type for TopHat2.")
parser.add_argument("--singleend", help = "The RNA-Seq data is single-ended.", default = "False")
args = parser.parse_args()

print args.MEM
print args.out

for line in fileinput.input("-"):
	line = line.rstrip()
	script_path = "/nfs/users/nfs_k/ka8/software/utils/tophat2-align.py"
	output_dir = os.path.join(args.out, line)

	#If paired end create two fastq files
	if (args.singleend == "False"):
		fq1 = os.path.join(args.fastq, line + ".1.fq.gz")
		fq2 = os.path.join(args.fastq, line + ".2.fq.gz")
		fq = [fq1, fq2]
	#If single-end create only 1 file
	elif (args.singleend == "True"):
		fq = [os.path.join(args.fastq, line + ".fq.gz")]
	
	#Create output dir if it does not exist
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)
	arguments = ["--MEM", args.MEM, "--out", output_dir, "--ncores", args.ncores, "--queue", args.queue]
	if args.library:
		arguments = arguments + ["--library " + args.library]
	command = " ".join([script_path] + arguments + fq)
	print(command)
	os.system(command)
