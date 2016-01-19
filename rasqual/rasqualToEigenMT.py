import sys
import os
import argparse
import fileinput
import subprocess
from scipy import stats
from numpy import fromstring

parser = argparse.ArgumentParser(description = "Convert RASQUAL output into a format suitable for eigenMT.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--rasqualOut", help = "Path to the RASQUAL output file.")
args = parser.parse_args()

rasqual_file = open(args.rasqualOut)
print "\t".join(["snps","gene","statistic","pvalue","FDR","beta"])
for line in rasqual_file:
	line = line.rstrip()
	fields = line.split("\t")
	#Calculate p-value:
	chi_stat = float(fields[5])
	p_value = stats.chi2.sf(chi_stat, 1)
	snp = "\t".join([fields[1], fields[0], fields[5], str(p_value), str(p_value), fields[6]])
	print(snp)