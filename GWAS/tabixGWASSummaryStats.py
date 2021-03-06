import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Tabix index GWAS summary statisitics.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Path to the input directory of the summary stats.")
args = parser.parse_args()

#Iterate over GWAS names from STDIN
for line in fileinput.input("-"):
	gwas_name = line.rstrip()
	input_file = os.path.join(args.indir, gwas_name + ".txt.gz")
	sorted_file = os.path.join(args.indir, gwas_name + ".sorted.txt")
	compressed_file = sorted_file + ".gz"

	#print header
	header_command = " ".join(["zcat", input_file, "| head -n1 >", sorted_file])
	print(header_command)
	subprocess.call(['bash','-c',header_command])

	#Sort
	sort_command = " ".join(["zcat", input_file, "| tail -n+2 | sort -k2,2 -k3,3n >>", sorted_file])
	print(sort_command)
	subprocess.call(['bash','-c',sort_command])

	#Compress command
	compress_command = " ".join(["bgzip -f", sorted_file])
	print(compress_command)
	subprocess.call(['bash','-c',compress_command])

	#Index command
	tabix_command = " ".join(["tabix -s2 -b3 -e3 -f -S1", compressed_file])
	print(tabix_command)
	subprocess.call(['bash','-c',tabix_command])

