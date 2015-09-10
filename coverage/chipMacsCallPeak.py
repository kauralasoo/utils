import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Call peaks from ATAC-Seq BAM files", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input files.")
parser.add_argument("--outdir", help = "Directory of the output files.")
parser.add_argument("--insuffix", help = "Suffix of the input bam file.", default = ".no_duplicates.bam")
parser.add_argument("--control", help = "Path to the input file.", default = "-25")
parser.add_argument("--q", help = "MACS2 q parameter.", default = "0.01")
parser.add_argument("--broad", help = "Run MACS2 in broad mode.", default = "False")
parser.add_argument("--bampe", help = "Run MACS2 with the BAMPE format flag.", default = "False")
parser.add_argument("--execute", help = "If True then executes the command, otherwise just prints it out.", default  = "True")

args = parser.parse_args()

#Iterate over all ids
for line in fileinput.input("-"):
	line = line.rstrip()
	bam_file = os.path.join(args.indir, line, line + args.insuffix)
	outdir = os.path.join(args.outdir, line)
	command = " ".join(["macs2 callpeak -t", bam_file, "-c", args.control, "-q", args.q, "--outdir", outdir, "-n", line])
	if (args.broad == "True"):
		command = command + " --broad"
	if (args.bampe == "True"):
		command = command + " -f BAMPE"
	print(command)
	if (args.execute == "True"):
		subprocess.call(['bash','-c',command])
