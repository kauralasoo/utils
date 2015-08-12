import sys
import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Sort a list of BAM files by coordinate.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input BAM files.")
parser.add_argument("--outdir", help = "Directory of the output BAM files.")
parser.add_argument("--insuffix", help = "Suffix of the input bam file.", default = ".bam")
parser.add_argument("--outsuffix", help = "Suffix of the output bam file.", default = ".sortedByCoord.bam")
args = parser.parse_args()

#Construct file names
for line in fileinput.input("-"):
		sample_name = line.rstrip()
		path_in = os.path.join(args.indir, sample_name, sample_name + args.insuffix)
		path_out = os.path.join(args.outdir, sample_name, sample_name + args.outsuffix)
		command = "".join(["bamsort I=", path_in, " O=", path_out, " index=1"])
		print(command)
		subprocess.call(['bash','-c',command])


