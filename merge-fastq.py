import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Merge fastq files from multiple runs into single experiment.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input SRA files.")
parser.add_argument("--outdir", help = "Directory of the output FASTQ files.")
args = parser.parse_args()

experiment_run_dict = dict()
for line in fileinput.input("-"):
	id = line.rstrip()
	fields = id.split("\t")
	if(fields[0] in experiment_run_dict):
		experiment_run_dict[fields[0]].append(fields[1])
	else:
		experiment_run_dict[fields[0]] = [fields[1]]

for exp in experiment_run_dict.keys():
	runs = experiment_run_dict[exp]
	files = [os.path.join(args.indir, run + ".fastq.gz") for run in runs]
	exp_file = os.path.join(args.outdir, exp + ".fastq.gz")
	command = " ".join(["zcat"] + files + ["| gzip > ", exp_file])
	print(command)
	subprocess.call(['bash','-c',command])

