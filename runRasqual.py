import sys
import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Run RASQUAL on a list of genes.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--readCounts", help = "Binary matrix containing read counts in each sample.")
parser.add_argument("--offsets", help = "Binary matrix with sample-specific offsets.")
parser.add_argument("--n", help = "Number of samples.")
parser.add_argument("--vcf", help = "Path to the VCF file with ASE counts")
parser.add_argument("--geneids", help = "List of gene ids in the same order as in the counts matrix.")
parser.add_argument("--geneMetadata", help = "Matrix with the coordinates of the cis region; number of cis SNPs and fSNPs for each gene.")
parser.add_argument("--featureCoords", help = "Matrix containing comma-separated start/end coordinates for each feature.")
parser.add_argument("--execute", help = "Execute the script", default = "False")
args = parser.parse_args()

#Check that none of the required arguments is empty
if args.geneids == None:
	sys.exit("--geneids is a required parameter.")
if args.readCounts == None:
	sys.exit("--readCounts is a required parameter.")
if args.offsets == None:
	sys.exit("--offsets is a required parameter.")
if args.n == None:
	sys.exit("--n is a required parameter.")
if args.vcf == None:
	sys.exit("--vcf is a required parameter.")
if args.geneMetadata == None:
	sys.exit("--geneMetadata is a required parameter.")
if args.featureCoords == None:
	sys.exit("--featureCoords is a required parameter.")

#Import gene IDs into a dict:
gene_dict = dict()
gene_file = open(args.geneids,"r")
it = 1
for gene_id in gene_file:
	gene_id = gene_id.rstrip()
	gene_dict[gene_id] = it
	it = it + 1

#Import gene_metadata into a dict
metadata_dict = dict()
metadata_file = open(args.geneMetadata, "r")
header = metadata_file.readline()
for gene in metadata_file:
	fields = gene.rstrip().split("\t")
	metadata_dict[fields[0]] = fields

#Import feature coordinates into a dict
feature_coords = dict()
feature_coords_file = open(args.featureCoords, "r")
for line in feature_coords_file:
	fields = line.rstrip().split("\t")
	feature_coords[fields[0]] = fields[1:3]

#Iterate over gene_ids and run RASQUAL
for line in fileinput.input("-"):
	gene_ids = line.rstrip().split(",")
	for gene_id in gene_ids:
		feature_number = gene_dict[gene_id]

		#Parse gene meta data
		gene_meta = metadata_dict[gene_id]
		cis_window = gene_meta[1] + ":" + gene_meta[2] + "-" + gene_meta[3]
		n_feature_snps = gene_meta[4]
		n_cis_snps = gene_meta[5]
		feature_start = feature_coords[gene_id][0]
		feature_end = feature_coords[gene_id][1]

		tabix_command = " ".join(["tabix", args.vcf, cis_window])
		rasqual_command = " ".join(["rasqual -y", args.readCounts, "-k", args.offsets, "-n", args.n, "-j", str(feature_number), 
			"-f", gene_id, "-l", n_cis_snps, "-m", n_feature_snps, "-s", feature_start, "-e", feature_end, "-t -z"])
		command = tabix_command + " | " + rasqual_command
		print(command)




