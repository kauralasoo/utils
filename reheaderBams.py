import fileinput
import os
import sys
import argparse
import subprocess

parser = argparse.ArgumentParser(description = "Move BAMS from tophat2 folders to single folder and rename.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Path to directory of input bam files.")
parser.add_argument("--outdir", help = "Path to directory of output bam files.")
parser.add_argument("--new_header", help = "Path to new header file.")
parser.add_argument("--execute", help = "Execute the script", default = "False")
args = parser.parse_args()

for line in fileinput.input("-"):	
	line = line.rstrip()
	bam_file = line + ".bam"
	infile = os.path.join(args.indir, bam_file)
	outfile = os.path.join(args.outdir, bam_file)
	command = " ".join(["samtools reheader", args.new_header, infile, ">", outfile])
	print(command)
	if args.execute == "True":
		subprocess.call(['bash','-c',command])