import sys
import os
import argparse

parser = argparse.ArgumentParser(description = "Sort a folder of BAM files by read name.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input BAM files.")
parser.add_argument("--outdir", help = "Directory of the output BAM files.")
parser.add_argument("--nsuffix", help = "Number of characters in the suffix.", default = 10)
args = parser.parse_args()

#Construct file names
bams = os.listdir(args.indir)
bams = [bam[0:-int(args.nsuffix)] for bam in bams] #subtract extension
paths_in = [os.path.join(args.indir, id + ".bam") for id in bams]
paths_out = [os.path.join(args.outdir, id + ".nsort.bam") for id in bams]

#Iterate over bam files and sort
for (input, output) in zip(paths_in, paths_out):
	command = " ".join(["samtools sort -n -m 5000000000", input, output])
	print(command)
	os.system(command)
