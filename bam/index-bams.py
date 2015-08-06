import sys
import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Index bam files using samtools.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--bamdir", help = "Directory of the BAM files.")
parser.add_argument("--insuffix", help = "Suffix of the input bam file.", default = ".bam")
parser.add_argument("--execute", help = "Execute the script", default = "False")
args = parser.parse_args()

#Construct file names
for line in fileinput.input("-"):
		sample_name = line.rstrip()
		path_in = os.path.join(args.bamdir, sample_name, sample_name + args.insuffix)
		command = " ".join(["samtools index", path_in])
		print(command)
		if args.execute == "True":
			subprocess.call(['bash','-c',command])