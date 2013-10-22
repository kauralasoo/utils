import os
import sys
import argparse
import fileinput

parser = argparse.ArgumentParser(description = "Merge insert distribution estimates into one file.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--insert", help = "Path to the insert-dist folder", default = "miso/insert-dist/")
parser.add_argument("--outfile", help = "Path to the output file")
args = parser.parse_args()

for line in fileinput.input("-"):
	line = line.rstrip()
	insert_dist_file = os.path.join(args.insert, line + ".bam.insert_len")
	handle = open(insert_dist_file)
	text = handle.readline()
	handle.close()
	fields = text.split(",")
	mean = fields[0].split("=")[1]
	sd = fields[1].split("=")[1]
	print("\t".join([line, mean, sd]))

