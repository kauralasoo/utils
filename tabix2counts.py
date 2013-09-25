import os
import sys
import argparse
import fileinput

parser = argparse.ArgumentParser(description = "Convert BAM files to Tabix files", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--chrnames", help = "Path to file containing chromosome names", 
	default = "/nfs/users/nfs_k/ka8/group-scratch/kaur/annotations/GRCh37/bowtie2-index/chromosome_names.txt")
parser.add_argument("--tbxs", help = "Path to TABIX files", default = "tbxs")
parser.add_argument("--counts", help = "Path to count files", default = "counts")
parser.add_argument("--annotations", help = "Path to annotations in Natsuhiko format", 
	default = "/nfs/users/nfs_k/ka8/group-scratch/kaur/annotations/GRCh37/Ensembl_69/nk5/")
args = parser.parse_args()

#Read chromosome names from disk
chrnames_file = open(args.chrnames)
chrnames = chrnames_file.readlines()
chrnames = [chr.rstrip() for chr in chrnames]

#Iterate over all ids
for line in fileinput.input("-"):
	line = line.rstrip()
	tabix_file = os.path.join(args.tbxs, line + ".tbx.gz")
	count_file = os.path.join(args.counts, line + ".gz")
	for chrom in chrnames:
		annot_file = os.path.join(args.annotations, "chr" + chrom + ".gz")
		command = " ".join(["tabix", tabix_file, chrom, "| /nfs/users/nfs_n/nk5/bin/countReadChrom", annot_file, "| gzip >>", count_file])
		print command
		os.system(command)
#tabix tbxs/10506_0#1.tbx.gz ERCC-00171 | /nfs/users/nfs_n/nk5/bin/countReadChrom ../../annotations/GRCh37/Ensembl_69/nk5/ERCC-00171.gz -exon | gzip > 1.gz