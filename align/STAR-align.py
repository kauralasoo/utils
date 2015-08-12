#! /usr/bin/python2.7
# Script to fetch reads from irods and convert them to Fastq
import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Align RNA-Seq reads using STAR.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--outputDir", help = "Path to output directory.")
parser.add_argument("--fastqDir", help = "Directory of the fastq files.")
parser.add_argument("--genomeDir", help = "Path to the genome index.")
parser.add_argument("--runThreadN", help = "Number of cores to use.", default = "1")
parser.add_argument("--suffix", help = "suffix of the FASTQ file,", default = ".fastq.gz")

args = parser.parse_args()

for line in fileinput.input("-"):
	sample_id = line.rstrip()
	standard_flags =  "--readFilesCommand zcat --outSAMtype BAM Unsorted SortedByCoordinate --outWigType bedGraph --outWigStrand Stranded --outWigNorm RPM --limitBAMsortRAM 10000000000"
	out_folder = os.path.join(args.outputDir, sample_id)
	if not os.path.exists(out_folder):
		os.makedirs(out_folder)
	out_prefix = os.path.join(out_folder, sample_id + ".")
	read1_file = os.path.join(args.fastqDir, sample_id + ".1" + args.suffix)
	read2_file = os.path.join(args.fastqDir, sample_id + ".2" + args.suffix)
	command = " ".join(["STAR", "--runThreadN", args.runThreadN, "--genomeDir", args.genomeDir, "--outFileNamePrefix", out_prefix, "--readFilesIn", read1_file, read2_file, standard_flags])
	print(command)
	subprocess.call(['bash','-c',command])
