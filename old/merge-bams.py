import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Merge BAM/CRAM files into bam files from multiple runs into single sample.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input FASTQ files.")
parser.add_argument("--outdir", help = "Directory of the output FASTQ files.")
parser.add_argument("--insuffix", help = "Directory of the output FASTQ files.", default = ".cram")
parser.add_argument("--outsuffix", help = "Directory of the output FASTQ files.", default = ".bam")
args = parser.parse_args()

for line in fileinput.input("-"):
	map = line.rstrip()
	fields = map.split("\t")
	sample_name = fields[0]
	file_names = fields[1].split(";")

	#Construct file names from ids
	sample_file = os.path.join(args.outdir, sample_name + args.outsuffix)
	files = [os.path.join(args.indir, file_name + args.insuffix) for file_name in file_names]
	
	command = " ".join(["~/software/bin/samtools merge", sample_file] + files)
	print(command)
	subprocess.call(['bash','-c',command])

