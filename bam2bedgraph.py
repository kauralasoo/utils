import os
import sys
import argparse
import fileinput

parser = argparse.ArgumentParser(description = "Convert BAM file to a BedGraph file using bedtools", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--bams", help = "Path to BAM files", default = "bams_tophat2")
parser.add_argument("--bedgraphs", help = "Path to BedGraph files", default = "BedGraph")
parser.add_argument("--bigwig", help = "Path to BigWig files", default = "BigWig")
parser.add_argument("--chrlengths", help = "Path to gene annotations in GTF format", 
	default = "/nfs/users/nfs_k/ka8/group-scratch/kaur/annotations/GRCh37/bowtie2-index/chrom-sizes.txt")
parser.add_argument("--execute", help = "If True then executes the command, otherwise just prints it out.", default  = "True")
args = parser.parse_args()

#Iterate over all ids
for line in fileinput.input("-"):
	line = line.rstrip()
	bam_file = os.path.join(args.bams, line + ".bam")
	bg_file = os.path.join(args.bedgraphs, line + ".bg")
	bw_file = os.path.join(args.bigwig, line + ".bw")
	command = " ".join(["bedtools genomecov -bga -split -ibam", bam_file, "-g", args.chrlengths, ">", bg_file])
	bw_command = " ".join(["bedGraphToBigWig", bg_file, args.chrlengths, bw_file])
	print(command)
	print(bw_command)
	if (args.execute == "True"):
		os.system(command)
		os.system(bw_command)