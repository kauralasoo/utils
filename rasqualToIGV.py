import sys
import os
import argparse
import fileinput
import subprocess
from scipy import stats
from numpy import fromstring

parser = argparse.ArgumentParser(description = "Convert RASQUAL output into a format suitable for IGV.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--rasqualOut", help = "Path to the RASQUAL output file.")
parser.add_argument("--geneid", help = "ID of the gene of interest.")
args = parser.parse_args()

rasqual_file = open(args.rasqualOut)
print "\t".join(["CHR","BP","SNP","P"])
for line in rasqual_file:
	line = line.rstrip()
	fields = line.split("\t")
	if fields[0] == args.geneid:
		#Calculate p-value:
		chi_stat = float(fields[10])
		p_value = stats.chi2.sf(chi_stat, 1)
		snp = "\t".join([fields[2],fields[3], fields[1], str(p_value)])
		print(snp)