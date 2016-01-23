import sys
import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Run eigenMT.py on RASQUAL output chomosome-by-chromosome, takes chromosome names from STDIN.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--metadata_dir", help = "Directory containing SNP and gene positions as well as genotype matrices.")
parser.add_argument("--chr_prefix", help = "Prefix of the genptype and snp position files.", default = "chr_")
parser.add_argument("--QTL", help = "Output file from matrixEQTL or rasqualToEigenMT.py")
parser.add_argument("--out_prefix", help = "Prefix of the output file.")
parser.add_argument("--cis_dist", help = "Width of th cis distance around features.")
parser.add_argument("--eigenMT_path", help = "Path to the eigenMT.py script.", default = "~/software/eigenMTwithTestData/eigenMT_fixed.py")
args = parser.parse_args()


#Iterate over chromosomes from STDIN
for line in fileinput.input("-"):
	chr_name = line.rstrip()
	genotype_matrix = os.path.join(args.metadata_dir, args.chr_prefix + chr_name + ".genotypes.txt")
	gene_pos_matrix = os.path.join(args.metadata_dir, "gene_positions.txt")
	snp_pos_matrix = os.path.join(args.metadata_dir, args.chr_prefix + chr_name + ".snp_positions.txt")
	output_file = ".".join([args.out_prefix, args.chr_prefix + chr_name, "eigenMT.txt"])
	command = " ".join(["python", args.eigenMT_path, "--CHROM", chr_name, "--QTL", args.QTL, "--GEN", genotype_matrix, "--GENPOS", snp_pos_matrix, "--PHEPOS", gene_pos_matrix, "--OUT" , output_file, "--cis_dist", args.cis_dist, "--external"])
	print(command)
	subprocess.call(['bash','-c',command])
