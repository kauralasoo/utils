import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Filter VCF file to keep only SNPs", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--vcfSuffix", help = "Suffix of the VCF file.", default = ".vcf.gz")
parser.add_argument("--indir", help = "Path to the input directory.")
parser.add_argument("--outdir", help = "Path to the output directory.")
parser.add_argument("--execute", help = "If True then executes the command, otherwise just prints it out.", default  = "True")
args = parser.parse_args()

for line in fileinput.input("-"):
	vcf_base_name = line.rstrip()
	input_vcf = os.path.join(args.indir, vcf_base_name + args.vcfSuffix)
	output_vcf = os.path.join(args.outdir, vcf_base_name + ".snps_only" + args.vcfSuffix)

	#Set up a bcftools pipeline to perform basic filtering
	command = " ".join(["bcftools view -O z --types snps", input_vcf, ">", output_vcf])
	print(command)

	if (args.execute == "True"):
		subprocess.call(['bash','-c',command])
