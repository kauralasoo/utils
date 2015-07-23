import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Iterate thorugh a sorted VCF file and detect SNPs with indentical coorinates.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--vcf", help = "Path to the vcf file.")
parser.add_argument("--duplicates", help = "Path to duplicates file.")
args = parser.parse_args()

vcf_file = open(args.vcf)
last_line = ""
last_coord = ['0','0']
last_fields = ""
dup_file = open(args.duplicates,'w')
for line in vcf_file:
	line = line.rstrip()
	if (line[0] == "#"):
		print line
	else:
		fields = line.split("\t")
		new_coord = fields[0:2]
		if new_coord != last_coord:
			#If the last line is not empty then print it
			if last_line != "":
				print last_line
			#Update last line
			last_coord = new_coord
			last_line = line
			last_fields = fields
		else: #Last line and new line have same coordinades
			last_alt = last_fields[4]
			new_alt =  fields[4]
			#Write all duplicates to a file
			dup_file.write(last_line +"\n")
			dup_file.write(line +"\n")
			#If one of the SNPs is multiallelic and the other is not then keep the biallelic
			if len(last_alt) > 1 & len(new_alt) == 1:
				print(line)
			elif len(new_alt) > 1 & len(last_alt) == 1:
				print(last_line)
			#If one of SNP is imputed and the other one is measured then prefer the imputed one, because its more likely to have correct ALT allele
			elif len(last_fields[8]) < len(fields[8]):
				print(last_line)
			elif len(fields[8]) < len(last_fields[8]):
				print(line)
			#Set to empty string so that it would not be printed at the next iteration of the loop
			last_line = ""
if last_line != "":
	print last_line
