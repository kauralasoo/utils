import sys
import os
import argparse
import fileinput
import subprocess
import gzip

parser = argparse.ArgumentParser(description = "Filter fastqtl output file by maximum p-value.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--fastqtl", help = "Path to the fastqtl output file with snp coordinates.")
parser.add_argument("--gene_id", help = "ID of the gene to be extracted from the file.")
args = parser.parse_args()

#print "CHR BP SNP P"
command1 = 'printf "CHR BP SNP P\n"'
command = " ".join(["zgrep", args.gene_id, args.fastqtl, '| cut -f2,3,4,6 -d " "'])
subprocess.call(['bash','-c',command1])
subprocess.call(['bash','-c',command])

