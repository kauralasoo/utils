import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Parse Bioanalyser export file into a table.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--infile", help = "Path to input file.")
args = parser.parse_args()

file = open(args.infile)
sample_list = list()
current_sample = ["sample_id", "ng_ul", "RIN"]
for line in file:
	line = line.rstrip()
	fields = line.split(",")
	if fields[0] == "Sample Name":
		sample_list.append(current_sample)
		current_sample = ["","",""]
		current_sample[0] = fields[1]
	if fields[0] == "RNA Concentration:":
		current_sample[1] = fields[1]
	if fields[0] == "RNA Integrity Number (RIN):":
		current_sample[2] = fields[1].split(" ")[0]
sample_list.append(current_sample)

for sample in sample_list:
	if sample[0] != "Ladder":
		print "\t".join(sample)
