import sys
import os
import argparse
import fileinput
import subprocess
import gzip

parser = argparse.ArgumentParser(description = "Add snp coordinates to fastQTL p-values file.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--vcf", help = "Path to the genotype VCF file.")
parser.add_argument("--fastqtl", help = "Path to the phenotype bed file.")
args = parser.parse_args()

vcf_file = gzip.open(args.vcf)
fastqtl_file = gzip.open(args.fastqtl)

variant_pos_dict = dict()
for line in vcf_file:
	if line[0] != "#":
		fields = line.split("\t")
		variant_pos_dict[fields[2]] = fields[0:2]

for line in fastqtl_file:
	line = line.rstrip()
	fields = line.split(" ")
	snp_id = fields[1]
	coords = variant_pos_dict[snp_id]
	#coords = ["1","1111"]
	line = " ".join([fields[0], coords[0], coords[1], fields[1], fields[2],fields[3],fields[4]])
	print(line)

