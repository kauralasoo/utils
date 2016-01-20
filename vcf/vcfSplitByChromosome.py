import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Split single VCF into multiple files by chormosome. Takes chromosome names as STDIN.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--vcf", help = "Path to the input VCF file (bcftools indexed).")
parser.add_argument("--outdir", help = "Output directory for the new vcf file.")
parser.add_argument("--outPrefix", help = "Prefix of the output VCF file.", default = "chr_")
parser.add_argument("--outSuffix", help = "Suffix of the output VCF file.", default = ".vcf.gz")
parser.add_argument("--execute", help = "If True then executes the command, otherwise just prints it out.", default  = "True")
args = parser.parse_args()

for line in fileinput.input("-"):
	chr_name = line.rstrip()
	output_file = os.path.join(args.outdir, args.outPrefix + chr_name + args.outSuffix)
	command = " ".join(["bcftools view -O z -r", chr_name, args.vcf, ">", output_file])
	print(command)

	if (args.execute == "True"):
		subprocess.call(['bash','-c',command])