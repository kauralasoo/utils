import sys
import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Test how many reads map to the mycoplasma genome.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--inputDir", help = "Directory of the input fastq files")
parser.add_argument("--outdir", help = "Directory of the output BED files.")
parser.add_argument("--insuffix", help = "Suffix of the input bam file.", default = ".1.fastq.gz")
parser.add_argument("--outsuffix", help = "Suffix of the output bam file.", default = ".mycoplasma.txt")
parser.add_argument("--bwaIndex", help = "BWA index base.")
parser.add_argument("--execute", help = "Execute the script", default = "False")
args = parser.parse_args()

#Construct file names
for line in fileinput.input("-"):
		sample_name = line.rstrip()
		path_in = os.path.join(args.inputDir, sample_name + args.insuffix)
		path_out = os.path.join(args.outdir, sample_name, sample_name + args.outsuffix)
		bedpe_to_bed = "python ~/software/utils/bedpe2bed.py --maxFragmentLength 1000 | sort -k 1,1 | gzip"
		command = " ".join(["bwa mem -a", args.bwaIndex, path_in, "| cut -f3 | sort | uniq -c >", path_out])
		print(command)
		if args.execute == "True":
			subprocess.call(['bash','-c',command])
