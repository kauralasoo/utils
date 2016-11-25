import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Tabix index GWAS summary statisitics.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Path to the input directory of the summary stats.")
parser.add_argument("--outdir", help = "Path to the output directory of the GARFIELD p-values.")
args = parser.parse_args()

#Iterate over GWAS names from STDIN
for line in fileinput.input("-"):
	gwas_name = line.rstrip()
	sorted_file = os.path.join(args.indir, gwas_name + ".sorted.txt.gz")
	output_directory = os.path.join(args.outdir, gwas_name)

	if not os.path.exists(output_directory):
		os.makedirs(output_directory)

	#Iterate over chromosomes
	for i in range(1,23):
		chr_string = "chr" + str(i)
		output_file = os.path.join(output_directory, chr_string)
		tabix_command = " ".join(["tabix", sorted_file, str(i), "| cut -f 3,6 --output-delimiter ' ' >", output_file])
		print tabix_command
	output_header_file = os.path.join(output_directory, "chrchr")
	header_command = " ".join(["echo 'pos pval' >", output_header_file])
	print(header_command)
