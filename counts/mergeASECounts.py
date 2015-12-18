import sys
import os
import argparse
import subprocess
#This avoids the Broken pipe error when output is piped into head
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 

parser = argparse.ArgumentParser(description = "Take ASE counts from multiple samples and merge them into one file.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input count files.")
parser.add_argument("--sample_list", help = "Text file mapping sample names to file names (columns: genotype_id, sample_id).")
parser.add_argument("--suffix", help = "Suffix of the ASECounts file.")
args = parser.parse_args()

#Load sample names from disk
sample_list = list()
sample_names = list()
samples_file = open(args.sample_list)
for line in samples_file:
	line = line.rstrip()
	fields = line.split("\t")
	sample_list.append(fields)
	sample_names.append(fields[0])

#Make a list of empty counts
empty_counts = [('0','0') for i in range(len(sample_names))]

#Iterate through all the files
variant_dictionary = dict()
variant_list = list()
header = ""
for sample_number in range(len(sample_list)):
	file_name = os.path.join(args.indir, sample_list[sample_number][1], sample_list[sample_number][1] + args.suffix)
	sample_file = open(file_name, "r")
	header = sample_file.readline().rstrip().split("\t")
	for line in sample_file:
		line = line.rstrip()
		fields = line.split("\t")
		variant_id = tuple(fields[0:5]) #Only tuples can be used as keys for a dict
		allele_counts = tuple(fields[5:7])
		if (variant_id in variant_dictionary):
			variant_dictionary[variant_id][sample_number] = allele_counts
		else:
			new_counts = list(empty_counts)
			new_counts[sample_number] = allele_counts
			variant_dictionary[variant_id] = new_counts
			variant_list.append(variant_id)
	sample_file.close()


#Print out the dictionary
complete_header = "\t".join(header[0:5] + sample_names) + "\n"
sys.stdout.write(complete_header)
for variant in variant_list:
	allele_count = variant_dictionary[variant]
	allele_vector = [",".join(sample_ase) for sample_ase in allele_count]
	variant_line = "\t".join(list(variant) + allele_vector) + "\n"
	sys.stdout.write(variant_line)



