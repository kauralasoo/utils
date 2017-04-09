import sys
import os
import argparse
import fileinput
import subprocess
import gzip

parser = argparse.ArgumentParser(description = "Convert UKBB GWAS data to the unified format.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Path to the input directory of the summary stats.")
parser.add_argument("--outdir", help = "Path to the output directory of the top variants.")
args = parser.parse_args()

for line in fileinput.input("-"):
	gwas_name = line.rstrip()
	input_file = os.path.join(args.indir, gwas_name + ".out.gz")
	unified_file = os.path.join(args.outdir, gwas_name + ".unified.txt.gz")

	#Open input file
	infile = gzip.open(input_file, "r")
	header = infile.readline()

	#Open output file
	o = gzip.open(unified_file, "w")
	new_header = "\t".join(["RSid","Chr","Pos","Eff_allele","MAF","pval","beta","OR","log_OR","se","z.score","Disease","PubmedID","used_file"])
	o.write(new_header + "\n")

	for line in infile:
		line = line.rstrip().split("\t")

		rsid = line[0]
		chrom = line[2]
		pos = line[3]
		effect_allele = "NA"
		MAF = "NA"
		p_nominal = line[10]
		beta = line[8]
		OR = "NA"
		log_OR = "NA"
		se = line[9]
		z_score = "NA"
		trait = "CAD_2017"
		PMID = "NA"
		used_file = "NA"

		row = "\t".join([rsid, chrom, pos, effect_allele, MAF, p_nominal, beta, OR, log_OR, se, z_score, trait, PMID, used_file])
		o.write(row + "\n")
	o.close()
	infile.close()
