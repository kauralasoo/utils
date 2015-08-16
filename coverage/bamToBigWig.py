import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Convert a BAM file (single-end reads only) to BigWig using bedtools", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input files.")
parser.add_argument("--outdir", help = "Directory of the output files.")
parser.add_argument("--insuffix", help = "Suffix of the input bam file.", default = ".no_duplicates.bam")
parser.add_argument("--outsuffix", help = "Suffix of the output BigWig file.", default = ".bw")
parser.add_argument("--chrlengths", help = "Path to text file with chromosome lengths")
parser.add_argument("--execute", help = "If True then executes the command, otherwise just prints it out.", default  = "True")

args = parser.parse_args()

#Iterate over all ids
for line in fileinput.input("-"):
	line = line.rstrip()
	bed_file = os.path.join(args.indir, line, line + args.insuffix)
	bg_file = os.path.join(args.outdir, line, line + ".bg")
	bw_file = os.path.join(args.outdir, line, line + args.outsuffix)
	command = " ".join(["bedtools genomecov -bga -ibam", bed_file, "-g", args.chrlengths, ">", bg_file])
	bw_command = " ".join(["bedGraphToBigWig", bg_file, args.chrlengths, bw_file])
	gzip_command = " ".join(["gzip", bg_file])
	print(command)
	print(bw_command)
	print(gzip_command)
	if (args.execute == "True"):
		subprocess.call(['bash','-c',command])
		subprocess.call(['bash','-c',bw_command])
		subprocess.call(['bash','-c',gzip_command])

