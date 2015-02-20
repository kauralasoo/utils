import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Merge fastq files from multiple runs into single sample.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input FASTQ files.")
parser.add_argument("--outdir", help = "Directory of the output FASTQ files.")
parser.add_argument("--suffix", help = "Directory of the output FASTQ files.", default = ".fastq.gz")
parser.add_argument("--execute", help = "If True then executes the command, otherwise just prints it out.", default  = "True")
args = parser.parse_args()

for line in fileinput.input("-"):
	map = line.rstrip()
	fields = map.split("\t")
	sample_name = fields[0]
	file_names = fields[1].split(";")

	#Construct file names from ids
	sample_file = os.path.join(args.outdir, sample_name + args.suffix)
	files = [os.path.join(args.indir, file_name + args.suffix) for file_name in file_names]
	
	command = " ".join(["zcat"] + files + ["| gzip >", sample_file])
	print(command)
	if (args.execute == "True"):
		subprocess.call(['bash','-c',command])

