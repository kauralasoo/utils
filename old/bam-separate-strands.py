#Separate reads on plus and minus strands to two different BAMs.
import sys
import os
import argparse
import fileinput

parser = argparse.ArgumentParser(description = "Filter out plus or minus strand from a BAM file.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--strand", help = "Name of the strand to be kept: plus or minus.")
parser.add_argument("--indir", help = "Directory of input BAM files.", default = "bams_tophat2")
parser.add_argument("--outdir", help = "Directory of the output BAM files. Required.")
args = parser.parse_args()

for line in fileinput.input("-"):
	line = line.rstrip()
	inbam = os.path.join(args.indir, line + ".bam")
	outbam = os.path.join(args.outdir, line + ".bam")
	
	#Parse strand specification
	if args.strand == "plus":
		tag =  "-tag XS:+"
	elif args.strand == "minus":
		tag = "-tag XS:-"
	else:
		print "Invalid strand specification"
		exit()

	command = " ".join(["bamtools filter -in", inbam, tag, "-out", outbam])
	print(command)
	os.system(command)
