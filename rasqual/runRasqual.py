import sys
import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Run RASQUAL on a list of genes. The script expects two-column TAB-separared file in STDIN, where the first column contains batch id and the second column contains comma-separated list of gene ids. Example: batch_1\tATAC_peak_13421,ATAC_peak_13422", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--readCounts", help = "Binary matrix containing read counts in each sample (genes in rows, samples in columns).")
parser.add_argument("--offsets", help = "Binary matrix with sample-specific offsets (genes in rows, samples in columns).")
parser.add_argument("--covariates", help = "Binary matrix with covariates (samples in rows, covariates in columns).")
parser.add_argument("--n", help = "Number of samples.")
parser.add_argument("--vcf", help = "Path to the VCF file with ASE counts.")
parser.add_argument("--outprefix", help = "Prefix of the output file.")
parser.add_argument("--geneids", help = "List of gene ids in the same order as in the counts matrix.")
parser.add_argument("--geneMetadata", help = "Gene metadata matrix with the following columns (in the same order): gene_id, chromosome_name, strand, exon_starts, exon_ends, range_start, range_end, feature_snp_count, cis_snp_count. Values in range_start and range_end columns specify the start and end of the cis region.")
parser.add_argument("--execute", help = "Execute the script", default = "False")
parser.add_argument("--rasqualBin", help = "Path to the the RASQUAL binary.", default = "/nfs/users/nfs_n/nk5/Project/C/RASQUAL/master/bin/rasqual_mt_icc")
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
if args.outprefix == None:
	sys.exit("--outprefix is a required parameter.")

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

#Iterate over batches of gene ids and run RASQUAL
for line in fileinput.input("-"):
	line = line.rstrip().split("\t")
	batch_id = line[0]
	gene_ids = line[1].split(",")
	for gene_id in gene_ids:
		feature_number = gene_dict[gene_id]

		#Parse gene meta data
		gene_meta = metadata_dict[gene_id]
		cis_window = gene_meta[1] + ":" + gene_meta[5] + "-" + gene_meta[6]
		n_feature_snps = gene_meta[7]
		n_cis_snps = gene_meta[8]
		feature_start = gene_meta[3]
		feature_end = gene_meta[4]

		tabix_command = " ".join(["tabix", args.vcf, cis_window])
		rasqual_command = " ".join([args.rasqualBin, "-y", args.readCounts, "-k", args.offsets, "-n", args.n, "-j", str(feature_number), 
			"-f", gene_id, "-l", n_cis_snps, "-m", n_feature_snps, "-s", feature_start, "-e", feature_end, " -z"])
		if (args.covariates != None): #If specified, add covariates to the rasqual command
			rasqual_command = " ".join([rasqual_command, "-x", args.covariates])
		output_file = args.outprefix + "." + batch_id + ".txt"
		command = tabix_command + " | " + rasqual_command + " >> " + output_file
		sys.stdout.write(command + "\n")
		if (args.execute == "True"):
			subprocess.call(['bash','-c',command])




	
