#! /usr/bin/python2.7
import os
import sys
import argparse
import fileinput
import subprocess

#Parse command line arguments
parser = argparse.ArgumentParser(description = "Align RNA-Seq reads to the reference genome using TopHat2.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--index", help = "Bowtie2 index location.")
parser.add_argument("--txindex", help = "Tophat2 transcriptome index location.")
parser.add_argument("--out", help = "TopHat2 output folder.")
parser.add_argument("--ncores", help = "Number of cores to use.", default = "1")
parser.add_argument("--library", help = "library type for TopHat2.", default = "fr-firststrand")
parser.add_argument("--singleend", help = "The RNA-Seq data is single-ended.", default = "False")
parser.add_argument("--suffix", help = "The RNA-Seq data is single-ended.", default = ".fq.gz")
parser.add_argument("--fastq", help = "Path to folder containing FASTQ files")
parser.add_argument("--no_execute", help = "Do not execute the command", default = "False")
args = parser.parse_args()

#Set up TopHat arguments
for line in fileinput.input("-"):
	line = line.rstrip()

	outfolder = os.path.join(args.out, line)
	tophat2_arguments = ["tophat2",
					"--no-coverage-search", 
					"-o " + outfolder,
					"-p " + args.ncores,
					"--transcriptome-index " + args.txindex,
					"--library-type " + args.library]

	#If paired end create two fastq files
	if (args.singleend == "False"):
		fq1 = os.path.join(args.fastq, line + ".1" + args.suffix)
		fq2 = os.path.join(args.fastq, line + ".2" + args.suffix)
		fq = [fq1, fq2]
	#If single-end create only 1 file
	elif (args.singleend == "True"):
		fq = [os.path.join(args.fastq, line + ".fq.gz")]

	tophat2_command = " ".join(tophat2_arguments + [args.index] + fq)
	print(tophat2_command)
	if(args.no_execute == "False"):
		subprocess.call(['bash','-c',tophat2_command])




