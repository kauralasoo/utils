#! /usr/bin/python2.7
import os
import sys
import argparse
import subprocess
import fileinput


parser = argparse.ArgumentParser(description = "Run mmdiff with specfied file names and model.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#parser.add_argument("--model", help = "Path to model file.")
parser.add_argument("--samples", help = "Path to samples files.")
parser.add_argument("--sample_dir", help = "Path to dir where samples are stored.")
parser.add_argument("--output", help = "mmdiff output file.")
parser.add_argument("--ncores", help = "Number of cores to be used.", default = "1")
args = parser.parse_args()

#Construct list of samples
sample_list = list()
samples_file = open(args.samples)
for line in samples_file:
	line = line.rstrip()
	line = os.path.join(args.sample_dir, line)
	sample_list.append(line)

#Read models from stdin
for line in fileinput.input("-"):
	print(line)
	model = line.rstrip()
	model_base = os.path.basename(model)
	model_name = model_base.rsplit(".",1)[0]
	output_file = os.path.join(args.sample_dir, model_name + ".mmdiff")
	command = " ".join(["OMP_NUM_THREADS=" + args.ncores, "mmdiff -useprops -m", model]+ sample_list + [">", output_file])
	print(command)
	subprocess.call(['bash','-c',command])