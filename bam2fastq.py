# Convert sorted BAM files to fastq files
import sys
import os
import argparse
import fileinput

parser = argparse.ArgumentParser(description = "Convert sorted BAM files to fastq files. Read the sample ids from STDIN.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input BAM files.")
parser.add_argument("--outdir", help = "Directory of the output FASTQ files.")
parser.add_argument("--suffix", help = "Number of characters in the suffix.", default = ".nsort.bam")
args = parser.parse_args()

#Read input files from standard input
ids = list()
for line in fileinput.input("-"):
	id = line.rstrip()
	ids.append(id)

#Construct file names
bams = [os.path.join(args.indir, id + args.suffix) for id in ids]
paths_r1 = [os.path.join(args.outdir, id + ".1.fq") for id in ids]
paths_r2 = [os.path.join(args.outdir, id + ".2.fq") for id in ids]


#Iterate over bam files and sort
for (bam, r1, r2) in zip(bams, paths_r1, paths_r2):
	command = " ".join(["bamToFastq -i", bam, "-fq", r1, "-fq2", r2])
	print(command)
	os.system(command)

