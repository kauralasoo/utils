# Convert sorted BAM files to fastq files
import sys
import os
import argparse
import fileinput

parser = argparse.ArgumentParser(description = "Convert sorted BAM files to fastq files. Read the BAM file names from STDIN.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--outdir", help = "Directory of the output FASTQ files.")
parser.add_argument("--nsuffix", help = "Number of characters in the suffix.", default = 10)
args = parser.parse_args()

#Read input files from standard input
input_files = list()
ids = list()
for line in fileinput.input("-"):
	line = line.rstrip()
	input_files.append(line)
	id = os.path.basename(line)
	id = id[0:-int(args.nsuffix)] #Remove suffix from ID
	ids.append(id)

#Construct file names
paths_r1 = [os.path.join(args.outdir, id + ".1.fq") for id in ids]
paths_r2 = [os.path.join(args.outdir, id + ".2.fq") for id in ids]

#Iterate over bam files and sort
for (bam, r1, r2) in zip(input_files, paths_r1, paths_r2):
	command = " ".join(["bamToFastq -i", bam, "-fq", r1, "-fq2", r2])
	print(command)
	os.system(command)

