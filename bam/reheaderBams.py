import sys
import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Update the header of a list of bam files. Sample names from STDIN.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input BAM files.")
parser.add_argument("--outdir", help = "Directory of the output BAM files.")
parser.add_argument("--insuffix", help = "Suffix of the input bam file.", default = ".bam")
parser.add_argument("--outsuffix", help = "Suffix of the output bam file.", default = ".reheader.bam")
parser.add_argument("--newHeader", help = "Path to new header file", default = ".reheader.bam")
parser.add_argument("--execute", help = "Execute the script", default = "False")
args = parser.parse_args()

#Construct file names
for line in fileinput.input("-"):
		sample_name = line.rstrip()
		path_in = os.path.join(args.indir, sample_name, sample_name + args.insuffix)
		path_out = os.path.join(args.outdir, sample_name, sample_name + args.outsuffix)
		command = " ".join(["samtools reheader", args.newHeader, path_in, ">", path_out])
		print(command)
		if args.execute == "True":
			subprocess.call(['bash','-c',command])