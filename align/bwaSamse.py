#! /usr/bin/python2.7
# Script to fetch reads from irods and convert them to Fastq
import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Convert single-end SAI file into a BAM.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--outputDir", help = "Path to output directory.")
parser.add_argument("--fastqDir", help = "Directory of the fastq files.")
parser.add_argument("--genomeDir", help = "Path to the genome index.")
parser.add_argument("--fastqSuffix", help = "suffix of the FASTQ file,", default = ".fastq.gz")
parser.add_argument("--saiSuffix", help = "suffix of the SAI file,", default = ".sai")
parser.add_argument("--bamSuffix", help = "suffix of the BAM file,", default = ".aligned.bam")

args = parser.parse_args()

for line in fileinput.input("-"):
	sample_id = line.rstrip()
	out_folder = os.path.join(args.outputDir, sample_id)
	if not os.path.exists(out_folder):
		os.makedirs(out_folder)
	out_sai = os.path.join(out_folder, sample_id + args.saiSuffix)
	out_bam = os.path.join(out_folder, sample_id + args.bamSuffix)
	read_file = os.path.join(args.fastqDir, sample_id + args.fastqSuffix)
	read_group_id = '\'@RG\tID:1\tSM:'+ sample_id +'\tPL:Illumina\tLB:1\tPU:1\''
	command = " ".join(["bwa samse -r", read_group_id, args.genomeDir, out_sai, read_file, "| samtools view -b -F 4 - > ", out_bam])
	print(command)
	subprocess.call(['bash','-c',command])
