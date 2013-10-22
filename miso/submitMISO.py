import os
import sys
import argparse
import fileinput

parser = argparse.ArgumentParser(description = "Run MISO on multiple samples", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--inserts", help = "Path to the insert size distribution summary file")
parser.add_argument("--outfile", help = "Path to the output file")
parser.add_argument("--miso_index", help = "Path to miso index directory.", default = "miso/miso_index/")
parser.add_argument("--bams", help = "Path to BAM files.", default = "bams_tophat2")
parser.add_argument("--read_length", help = "Read length.", default = "75")
parser.add_argument("--output", help = "Path to output folder.", default = "miso/genes-psi/")
parser.add_argument("--chunks", help = "Number of genes in a chunk.", default = "500")
parser.add_argument("--settings", help = "Path to settings file.", default = "lps-response/miso/miso_settings.txt")
args = parser.parse_args()

#Build dictionaries of mean and sd values
mean_dict = dict()
sd_dict = dict()
for line in open(args.inserts):
	line = line.rstrip()
	fields = line.split("\t")
	mean_dict[fields[0]] = fields[1]
	sd_dict[fields[0]] = fields[2]

#Construct MISO command
for line in fileinput.input("-"):
	line = line.rstrip()
	paired_end = " ".join(["--paired-end", mean_dict[line], sd_dict[line]])
	compute = " ".join(["--compute-genes-psi", args.miso_index,  os.path.join(args.bams, line + ".bam"), "--use-cluster"])
	read_length = " ".join(["--read-len",args.read_length])
	output = "=".join(["--output-dir", os.path.join(args.output, line)])
	chunks = " ".join(["--chunk-jobs", args.chunks])
	settings = "=".join(["--settings-filename", args.settings])
	command = " ".join(["~/software/miso/misopy/run_events_analysis.py", compute, paired_end, read_length, settings, chunks, output])
	print(command)
	os.system(command)
