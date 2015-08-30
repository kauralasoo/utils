import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Call peaks from ATAC-Seq BAM files", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input files.")
parser.add_argument("--outdir", help = "Directory of the output files.")
parser.add_argument("--insuffix", help = "Suffix of the input bam file.", default = ".no_duplicates.bam")
parser.add_argument("--shift", help = "MACS2 shift parameter.", default = "-25")
parser.add_argument("--extsize", help = "MACS2 extsize parameter.", default = "50")
parser.add_argument("--q", help = "MACS2 q parameter.", default = "0.01")
parser.add_argument("--execute", help = "If True then executes the command, otherwise just prints it out.", default  = "True")

args = parser.parse_args()

#Iterate over all ids
for line in fileinput.input("-"):
	line = line.rstrip()
	bam_file = os.path.join(args.indir, line, line + args.insuffix)
	outdir = os.path.join(args.outdir, line)
	command = " ".join(["macs2 callpeak --nomodel -t", bam_file, "--shift", args.shift, "--extsize", args.extsize, "-q", args.q, "--outdir", outdir, "-n", line])
	print(command)
	if (args.execute == "True"):
		subprocess.call(['bash','-c',command])
