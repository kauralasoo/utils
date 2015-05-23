import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Convert a bedgraph file to a BigWig file", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input bedgraph files.")
parser.add_argument("--outdir", help = "Directory of the output bigwig files.")
parser.add_argument("--insuffix", help = "Suffix of the input bedgraph file.", default = ".Signal.Unique.str1.out.bg")
parser.add_argument("--outsuffix", help = "Suffix of the output bigwig file.", default = ".Signal.Unique.str1.out.bw")
parser.add_argument("--chrlengths", help = "Path to text file with chromosome lengths")
parser.add_argument("--execute", help = "If True then executes the command, otherwise just prints it out.", default  = "True")

args = parser.parse_args()

#Iterate over all ids
for line in fileinput.input("-"):
	line = line.rstrip()
	bg_file = os.path.join(args.indir, line, line + args.insuffix)
	bw_file = os.path.join(args.outdir, line, line + args.outsuffix)
	bw_command = " ".join(["bedGraphToBigWig", bg_file, args.chrlengths, bw_file])
	gzip_command = " ".join(["gzip", bg_file])
	print(bw_command)
	print(gzip_command)
	if (args.execute == "True"):
		subprocess.call(['bash','-c',bw_command])
		subprocess.call(['bash','-c',gzip_command])

