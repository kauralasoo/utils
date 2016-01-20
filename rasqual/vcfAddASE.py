import sys
import os
import argparse
import subprocess
#This avoids the Broken pipe error when output is piped into head
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 

parser = argparse.ArgumentParser(description = "Add ASE counts data into the VCF file.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--ASEcounts", help = "Path to the ASE counts file.")
parser.add_argument("--ASESampleGenotypeMap", help = "Text file mapping ASE sample names to genotype ids.")
parser.add_argument("--VCFfile", help = "Path to the VCF file.")
args = parser.parse_args()

#Read ASE sample names form counts file
ase_file = open(args.ASEcounts)
ase_header = ase_file.readline().rstrip().split("\t")
ase_sample_names = ase_header[5:]

#Read mapping to genptype ids
sg_map_file = open(args.ASESampleGenotypeMap)
sample_genptype_dict = dict()
for line in sg_map_file:
	line = line.rstrip()
	fields = line.split("\t")
	sample_genptype_dict[fields[0]] = fields[1]

#Construct a sample name dict
ase_sample_dict = dict()
for i in range(0,len(ase_sample_names)):
	if (ase_sample_names[i] in sample_genptype_dict):
		genotype_id = sample_genptype_dict[ase_sample_names[i]]
		ase_sample_dict[genotype_id] = i

#Construct a dictionary of ASE counts
ase_dict = dict()
for variant in ase_file:
	fields = variant.rstrip().split("\t")
	variant_id = tuple([fields[i] for i in [0,1,3,4]]) #Use CHR, POS, REF and ALT as the id of a variant.
	variant_counts = fields[5:]
	ase_dict[variant_id] = variant_counts

#Read sample name from the VCF file
sample_order = list()
variant_counter = 0
empty_counts = list()

vcf_file = open(args.VCFfile)
for line in vcf_file:
	line = line.rstrip()
	#Header
	if (line[0:2] == "##"):
		print(line.rstrip())
	#Sample names
	elif(line[0:6] == "#CHROM"):
		vcf_header = line.rstrip()
		vcf_samples = vcf_header.split("\t")[9:]
		empty_counts = ['0,0' for i in range(len(vcf_samples))]
		#Match the order of vcf sample names to the order of the ASE counts
		for sample in vcf_samples:
			if sample in ase_sample_dict:
				sample_order.append(ase_sample_dict[sample])
			else:
				sys.stderr.write("Sample " + sample + " not found in the ASEcounts file.")
				sys.exit()

		#Update header
		print '##FORMAT=<ID=AS,Number=.,Type=String,Description="Allele-specific expression counts from RNA-seq">' #Format tag
		print '##vcfAddASE_ASEcounts=' + args.ASEcounts #Edit trail
		print vcf_header #Sample names
	#Update VCF file
	else:
		fields = line.split("\t")
		#Add AS tag to the variant info field
		variant_info = fields[0:9]
		variant_info[8] = variant_info[8] + ":AS" 

		#Add AS counts to each variant
		variant_data = fields[9:]
		variant_id = tuple([fields[i] for i in [0,1,3,4]]) #Use CHR, POS, REF and ALT as the id of a variant.
		if variant_id in ase_dict:
			variant_counts = ase_dict[variant_id]
			#Ensure that ASE count and VCF file samples are in the same order
			variant_counts_reorder = [variant_counts[i] for i in sample_order] 
			variant_counter = variant_counter + 1
		else: #if no counts in dictionary assume zeros
			variant_counts_reorder = empty_counts

		#Print updated variant record
		variant_data_new = [(variant_data[i] + ":" + variant_counts_reorder[i]) for i in range(len(variant_data))]
		print "\t".join(variant_info + variant_data_new)

sys.stderr.write("Found counts for " + str(variant_counter) + " variants.\n")
