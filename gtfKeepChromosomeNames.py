import os
import sys
import argparse

parser = argparse.ArgumentParser(description = "Onle keep annotations that are on specifc chromosomes.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--chrnames", help = "Path to file containing chromosome names", 
	default = "/nfs/users/nfs_k/ka8/group-scratch/kaur/annotations/GRCh37/bowtie2-index/chromosome_names.txt")
parser.add_argument("--gtf", help = "Path to GTF file")
args = parser.parse_args()

chr_file = open(args.chrnames)
chromosomes = chr_file.readlines()
chromosomes = [chr.rstrip() for chr in chromosomes]
chrdict = dict(zip(chromosomes, [1]*len(chromosomes)))

gtf_file = open(args.gtf)
for line in gtf_file:
	line = line.rstrip()
	fields = line.split("\t")
	if fields[0] in chrdict:
		print line
