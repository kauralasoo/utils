import os
import sys
import argparse
import gffutils

parser = argparse.ArgumentParser(description = "Keep only those entries in a GFF file that are also present in the transcript table.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--GTFdb", help = "Path to GTF database file")
parser.add_argument("--txtable", help = "Path transcript table (two columns: gene_id, transcript_id; contains header row)")
args = parser.parse_args()

#Read gene and transcript IDs from disk
table_file = open(args.txtable)
gene_dictionary = dict()
transcript_dictionary = dict()
header = table_file.readline()
for line in table_file:
	line = line.rstrip()
	fields = line.split("\t")
	gene_dictionary[fields[0]] = 1
	transcript_dictionary[fields[1]] = 1
genes = gene_dictionary.keys() 

#Open GFF database
db = gffutils.FeatureDB(args.GTFdb)

for gene in genes:
	try:
		gene_record = db[gene]
		print(gene_record)
	except gffutils.FeatureNotFoundError:
		sys.stderr.write("ERROR: Gene " + gene +" not found in GFF file.\n")
		continue
	for isoform in db.children(gene_record, featuretype = "transcript"):
		isoform_id = isoform.attributes["transcript_id"][0] #Filter isoforms
		if isoform_id in transcript_dictionary:
			print(isoform)
			for exon in db.children(isoform, featuretype = "exon"):
				print(exon)
