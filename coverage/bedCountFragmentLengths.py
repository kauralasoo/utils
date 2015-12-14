import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Count the occurences of different fragment lengths in a BED file", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input files.")
parser.add_argument("--outdir", help = "Directory of the output files.")
parser.add_argument("--insuffix", help = "Suffix of the input BED file.", default = ".fragments.bed.gz")
parser.add_argument("--outsuffix", help = "Suffix of the output BigWig file.", default = ".fragment_lengths.txt")
parser.add_argument("--execute", help = "If True then executes the command, otherwise just prints it out.", default  = "True")
args = parser.parse_args()

#Iterate over all ids
for line in fileinput.input("-"):
	line = line.rstrip()
	bed_file = os.path.join(args.indir, line, line + args.insuffix)
	count_file = os.path.join(args.outdir, line, line + args.outsuffix)
	command = " ".join(["zcat", bed_file, "| cut -f5 | sort -n | uniq -c >", count_file])
	print(command)
	if (args.execute == "True"):
		subprocess.call(['bash','-c',command])

