import sys
import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Test for association between genotype and phenotype.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--vcf", help = "Path to the genotype VCF file.")
parser.add_argument("--bed", help = "Path to the phenotype bed file.")
parser.add_argument("--cov", help = "Path to the covariates txt file.")
parser.add_argument("--W", help = "Size of the cis window.")
parser.add_argument("--out", help = "Prefix of the output filess.")
parser.add_argument("--permute", help = "Number of permutations to perform.")
parser.add_argument("--execute", help = "Execute the script", default = "False")
args = parser.parse_args()

#Check for required paramters
if args.out == None:
	sys.exit("--out is a required parameter.")
if args.vcf == None:
	sys.exit("--vcf is a required parameter.")
if args.bed == None:
	sys.exit("--bed is a required parameter.")
if args.W == None:
	sys.exit("--W is a required parameter.")
if args.cov == None:
	sys.exit("--cov is a required parameter.")
if args.permute == None:
	sys.exit("--permute is a required parameter.")

#Construct file names
for line in fileinput.input("-"):
	chunk = line.rstrip()
	chunks = chunk.split(" ")
	print(chunks)
	outfile = args.out + ".chunk_" + chunks[0] + "_" + chunks[1] + ".txt.gz"
	command = " ".join(["fastQTL.1.165.linux --vcf", args.vcf, "--bed", args.bed, "--chunk", chunk, "--cov", args.cov, "--out", outfile, "--permute", args.permute, "-W", args.W])
	print(command)
	if args.execute == "True":
		subprocess.call(['bash','-c',command])