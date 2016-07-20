import gzip
import sys
import os
import argparse
import fileinput
import subprocess
from operator import methodcaller

parser = argparse.ArgumentParser(description = "Split leafcutter counts file into two matrices.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--leafcutter_out", help = "Path to leafcutter output file.")
parser.add_argument("--outprefix", help = "Prefix of the output files.")
args = parser.parse_args()

#Import leafcutter output file

leafcutter_file = gzip.open(args.leafcutter_out,'rb')
intron_counts_file = gzip.open(args.outprefix + ".intron_counts.txt.gz", 'wb')
cluster_counts_file = gzip.open(args.outprefix + ".cluster_counts.txt.gz", 'wb')

#Copy header
header = leafcutter_file.readline()
intron_counts_file.write(header)
cluster_counts_file.write(header)

#Iterate over lines in the input file
for line in leafcutter_file:
	line = line.rstrip()
	fields = line.split(" ")
	cluster_id = fields[0]
	counts = fields[1:len(fields)]

	#Split counts
	split_counts = map(methodcaller("split", "/"), counts)
	intron_counts = [x[0] for x in split_counts]
	cluster_counts = [x[1] for x in split_counts]

	#Export intron counts
	intron_line = " ".join([cluster_id] + intron_counts) +"\n"
	cluster_line = " ".join([cluster_id] + cluster_counts) +"\n"
	intron_counts_file.write(intron_line)
	cluster_counts_file.write(cluster_line)

#Close all of the connections
leafcutter_file.close()
intron_counts_file.close()
cluster_counts_file.close()

