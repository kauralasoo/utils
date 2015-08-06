import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Count the number of reads aligned to each chromosome.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input FASTQ files.")
parser.add_argument("--outdir", help = "Directory of the output FASTQ files.")
parser.add_argument("--insuffix", help = "Suffix of the bam files.", default = ".bam")
parser.add_argument("--outsuffix", help = "Suffix of the chr counts file.", default = ".chr_counts")
parser.add_argument("--subdir", help = "Specify if the samples are in a subdirectory or not.", default = "True")

args = parser.parse_args()

for line in fileinput.input("-"):
	sample_name = line.rstrip()
	if(args.subdir == "True"):
		bam_file = os.path.join(args.indir, sample_name, sample_name + args.insuffix)
		counts_file = os.path.join(args.outdir, sample_name, sample_name + args.outsuffix)
	else:
		bam_file = os.path.join(args.indir, sample_name + args.insuffix)
		counts_file = os.path.join(args.outdir, sample_name + args.outsuffix)

	command = " ".join(["samtools view", bam_file, "| cut -f3 | sort | uniq -c >", counts_file])
	print(command)
	subprocess.call(['bash','-c',command])