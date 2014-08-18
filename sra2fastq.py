import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Convert GEO sra files to gzipped fastq files. Read the sample ids from STDIN.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input SRA files.")
parser.add_argument("--outdir", help = "Directory of the output FASTQ files.")
args = parser.parse_args()

for line in fileinput.input("-"):
	id = line.rstrip()
	sra_file = os.path.join(args.indir, id + ".sra")
	command = " ".join(["fastq-dump --gzip --outdir", args.outdir, sra_file])
	print(command)
	subprocess.call(['bash','-c',command])
