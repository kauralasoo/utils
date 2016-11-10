import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Parse FINEMAP posterior probabilities from the log files.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--logDir", help = "Path to the directory of FINEMAP log files.")
args = parser.parse_args()

def parse_log(path):
	log_file = open(path)
	line_count = -1
	posterior_list = list()
	for line in log_file:
		line = line.rstrip()
		if line[0:7] == "- log10":
			fields = line.split(" : ")
			posterior_list.append(fields[1])
			line_count = 1
		if line_count > 0:
			line_count = line_count + 1
			if line_count > 3:
				if line_count < 10:
					fields = line.split(" -> ")
					posterior_list.append(fields[1])
	return posterior_list

#posterior_list = parse_log("results/logs/ATAC_peak_101916.log")
#print(posterior_list)

file_names = os.listdir(args.logDir)
for file_name in file_names:
	full_path = os.path.join(args.logDir, file_name)
	posterior_list = parse_log(full_path)
	if len(posterior_list) > 0:
		row = "\t".join([file_name] + posterior_list)
		print(row)
