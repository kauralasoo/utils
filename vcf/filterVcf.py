import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Filter VCF file by genotype and MAF", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--sampleList", help = "Text file with sample names to be retained.")
parser.add_argument("--MAF", help = "Minimum minor allele frequency of variants to be retained.")
parser.add_argument("--vcfSuffix", help = "Suffix of the VCF file.", default = ".vcf.gz")
parser.add_argument("--indir", help = "Path to the input directory.")
parser.add_argument("--outdir", help = "Path to the output directory.")
parser.add_argument("--execute", help = "If True then executes the command, otherwise just prints it out.", default  = "True")
args = parser.parse_args()

for line in fileinput.input("-"):
	vcf_base_name = line.rstrip()
	input_vcf = os.path.join(args.indir, vcf_base_name + args.vcfSuffix)
	selected_vcf = os.path.join(args.outdir, vcf_base_name + ".filtered" + args.vcfSuffix)

	#Set up a bcftools pipeline to perform basic filtering
	select_command = " ".join(["bcftools view -O z -S", args.sampleList, input_vcf])
	filter_command = "".join(["bcftools filter -O z -i 'MAF[0] >= ", args.MAF, "' -"])
	command = " ".join([select_command, "|", filter_command, ">", selected_vcf])
	print(command)

	if (args.execute == "True"):
		subprocess.call(['bash','-c',command])