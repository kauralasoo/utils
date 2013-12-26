import sys
import os
import argparse
import fileinput

parser = argparse.ArgumentParser(description = "Sort a folder of BAM files by read name.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input BAM files.")
parser.add_argument("--outdir", help = "Directory of the output BAM files.")
parser.add_argument("--insuffix", help = "Suffix of the input bam file.", default = ".bam")
args = parser.parse_args()

#Construct file names
for line in fileinput.input("-"):
		id = line.rstrip()
		path_in = os.path.join(args.indir, id + args.insuffix)
		path_out = os.path.join(args.outdir, id + ".nsort")
		command = " ".join(["samtools sort -n -m 10000000000", path_in, path_out])
		print(command)
		os.system(command)
	

