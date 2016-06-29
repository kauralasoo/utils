import sys
import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Run fgwas on pairs of summary statistics and annotations.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--input_dir", help = "Directory of the input GWAS summary files.")
parser.add_argument("--insuffix", help = "Suffix of the input GWAS summary files.", default = ".allchr.fgwasin_noext.gz")
parser.add_argument("--output_dir", help = "Directory of the output files.")
parser.add_argument("--execute", help = "Execute the script", default = "False")
args = parser.parse_args()

for line in fileinput.input("-"):
		line = line.rstrip()
		fields = line.split("\t")
		trait = fields[0]
		annotations = fields[1]
		summary_file = os.path.join(args.input_dir, trait + args.insuffix)
		output_file_prefix = os.path.join(args.output_dir, trait + "_" + annotations)
		command = " ".join(["fgwas -cc -i", summary_file, "-o", output_file_prefix, "-w", annotations])
		print(command)
		if args.execute == "True":
			subprocess.call(['bash','-c',command])