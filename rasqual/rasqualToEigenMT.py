import sys
import os
import argparse
import fileinput
import subprocess
from scipy import stats

parser = argparse.ArgumentParser(description = "Convert RASQUAL output into a format suitable for eigenMT. Extract relevant columns and convert chisq statistic into p-value", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--rasqualOut", help = "Path to the merged RASQUAL output file (genrated by mergeRasqualBatches.py).")
args = parser.parse_args()

rasqual_file = open(args.rasqualOut)
print "\t".join(["snps","gene","statistic","pvalue","FDR","beta"])
for line in rasqual_file:
	line = line.rstrip()
	fields = line.split("\t")
	snp_id = fields[1]
	gene_id = fields[0]
	pi = fields[8]
	#Calculate p-value:
	chi_stat = float(fields[7])
	p_value = stats.chi2.sf(chi_stat, 1)
	snp = "\t".join([snp_id, gene_id, str(chi_stat), str(p_value), str(p_value), pi])
	if (snp_id != "SKIPPED"): #Ignore skipped genes
		print(snp)