#TODO: get old version from git
import os
import sys
import argparse
import fileinput

parser = argparse.ArgumentParser(description = "Convert BAM file to a BedGraph file using bedtools", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input BAM files.")
parser.add_argument("--outdir", help = "Directory of the output BED files.")
parser.add_argument("--chrlengths", help = "Path to text file with chromosome lengths")
parser.add_argument("--execute", help = "If True then executes the command, otherwise just prints it out.", default  = "True")
parser.add_argument("--split", help = "Treat the alignments as split or not.", default  = "True")

args = parser.parse_args()

#Iterate over all ids
for line in fileinput.input("-"):
	line = line.rstrip()
	bam_file = os.path.join(args.bams, line + ".bam")
	bg_file = os.path.join(args.bedgraphs, line + ".bg")
	bw_file = os.path.join(args.bigwig, line + ".bw")
	if args.split == "True":
		command = " ".join(["bedtools genomecov -bga -split -ibam", bam_file, "-g", args.chrlengths, ">", bg_file])
	else:
		command = " ".join(["bedtools genomecov -bga -ibam", bam_file, "-g", args.chrlengths, ">", bg_file])

	bw_command = " ".join(["bedGraphToBigWig", bg_file, args.chrlengths, bw_file])
	print(command)
	print(bw_command)
	if (args.execute == "True"):
		os.system(command)
		os.system(bw_command)