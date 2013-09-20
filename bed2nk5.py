#! /usr/bin/python2.7
import os
import sys
import argparse

parser = argparse.ArgumentParser(description = "Convert BED file to Natsuhiko format", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--bed", help = "Path to BED file")
parser.add_argument("--nk5", help = "Folder of annotations in Natsuhiko format.")
args = parser.parse_args()

bed_file = open(args.bed)
last_chr = "1"
annotfile = open(os.path.join(args.nk5, last_chr), 'wa')
for line in bed_file:
	line = line.rstrip()
	fields = line.split("\t")
	fields[1] = str(int(fields[1]) + 1)
	string = "\t".join(fields[0:4])

	gene_start = int(fields[1])
	start = (fields[11]).rstrip(",").split(",")
	start = [int(coord) + gene_start for coord in start]

	length = (fields[10]).rstrip(",").split(",")
	length = [int(coord) - 1 for coord in length]
	
	s = list()
	e = list()
	for (st,le) in zip(start,length):
		s.append(str(st))
		e.append(str(st + le))
	s = ",".join(s) + ","
	e = ",".join(e) + ","
	coords = "\t".join(s+e)
	string = "\t".join([string,s, e])
	
	chrom = fields[0]
	if chrom == last_chr:
		annotfile.write(string + "\n")
	else:
		last_chr = chrom
		annotfile.close()
		annotfile = open(os.path.join(args.nk5, last_chr), 'wa')
		annotfile.write(string + "\n")

