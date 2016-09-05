#! /usr/bin/python2.7
import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Quantify transcript expression using Salmon.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--outputDir", help = "Path to output directory.")
parser.add_argument("--outputSubdir", help = "Path to output directory.")
parser.add_argument("--fastqDir", help = "Directory of the fastq files.")
parser.add_argument("--fastqSuffix", help = "suffix of the FASTQ file,", default = ".fastq.gz")
parser.add_argument("--index", help = "Path to the Salmon index.")
parser.add_argument("--libType", help = "Salmon library type.")
parser.add_argument("--geneMap", help = "Map transcript ids to gene ids.")
parser.add_argument("--nCores", help = "Number of cores to use.", default = "1")
args = parser.parse_args()

for line in fileinput.input("-"):
	sample_id = line.rstrip()
	out_folder = os.path.join(args.outputDir, sample_id, args.outputSubdir)
	if not os.path.exists(out_folder):
		os.makedirs(out_folder)

	#Make read files
	read1_file = os.path.join(args.fastqDir, sample_id + ".1" + args.fastqSuffix)
	read2_file = os.path.join(args.fastqDir, sample_id + ".2" + args.fastqSuffix)

	#Construct commpand
	salmon_command = " ".join(["salmon --no-version-check quant --seqBias --gcBias --libType", args.libType, "--index", args.index, "-1", read1_file, "-2", read2_file, "-p", args.nCores, "--geneMap", args.geneMap, "-o", out_folder])
	print(salmon_command)
	subprocess.call(['bash','-c',command])
