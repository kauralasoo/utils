import os
import sys
import argparse
import fileinput
import subprocess
import gzip

parser = argparse.ArgumentParser(description = "Extract all variants above some significance threshold from the GWAS summary stats.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Path to the input directory of the summary stats.")
parser.add_argument("--outdir", help = "Path to the output directory of the top variants.")
args = parser.parse_args()

#Iterate over GWAS names from STDIN
for line in fileinput.input("-"):
	gwas_name = line.rstrip()
	sorted_file = os.path.join(args.indir, gwas_name + ".sorted.txt.gz")
	top_file = os.path.join(args.outdir, gwas_name + ".top_hits.txt.gz")

	#Open the file and filter
	f = gzip.open(sorted_file)
	o = gzip.open(top_file, "w")
	header = f.readline()
	o.write(header)
	for line in f:
		fields = line.split("\t")
		if (float(fields[5]) < 1e-5):
			o.write(line)
	o.close()
	f.close()
	


