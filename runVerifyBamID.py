import sys
import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Test concordance between BAM and VCF files using verifyBamID.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--bamdir", help = "Directory of the BAM files.")
parser.add_argument("--insuffix", help = "Suffix of the input bam file.", default = ".bam")
parser.add_argument("--vcf", help = "Path to the VCF file.")
parser.add_argument("--execute", help = "Execute the script", default = "False")
args = parser.parse_args()

#Construct file names
for line in fileinput.input("-"):
		sample_name = line.rstrip()
		bam_path = os.path.join(args.bamdir, sample_name, sample_name + args.insuffix)
		out_prefix = os.path.join(args.bamdir, sample_name, sample_name + ".verifyBamID")
		command = " ".join(["verifyBamID.1.1.2 --vcf", args.vcf, "--bam", bam_path, "--out", out_prefix, "--best"])
		print(command)
		if args.execute == "True":
			subprocess.call(['bash','-c',command])