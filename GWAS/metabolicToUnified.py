import sys
import os
import argparse
import fileinput
import subprocess
import gzip

parser = argparse.ArgumentParser(description = "Convert metabolic GWAS summaries to unified format for coloc.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Path to the input directory of the summary stats.")
parser.add_argument("--outdir", help = "Path to the output directory of the top variants.")
args = parser.parse_args()

for line in fileinput.input("-"):
	gwas_name = line.rstrip()
	input_file = os.path.join(args.indir, gwas_name + ".meta.txt.gz")
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

		#Extraxt rsid and pos
		rsid = line[0]
		fields = rsid.split(":")
		pos = fields[1]
		chrom = (fields[0].split("chr"))[1]
		Eff_allele = "NA"
		MAF = "NA"
		pval = line[9]
		beta = line[4]
		OR = "NA"
		log_OR = "NA"
		se = line[5]
		z_score = line[8]
		Disease = gwas_name
		pubmed_id = "27668658"
		used_file = "NA"

		row = "\t".join([rsid, chrom, pos, Eff_allele, MAF, pval, beta, OR, log_OR, se, z_score, Disease, pubmed_id, used_file])
		o.write(row + "\n")
	o.close()
	infile.close()
