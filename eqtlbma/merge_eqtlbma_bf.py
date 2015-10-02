import sys
import os
import argparse
import fileinput
import subprocess
import gzip

parser = argparse.ArgumentParser(description = "Wrapper script to run eqtlbma_bf command.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--outdir", help = "Directory of the eqtlbma output files.")
parser.add_argument("--outprefix", help = "Prefix of the output files.")
parser.add_argument("--geneBatches", help = "Text file containing batch ids.")
parser.add_argument("--suffix", help = "Suffix of the results file.", default = "_l10abfs_raw.txt.gz")
args = parser.parse_args()

if args.outdir == None:
	sys.exit("--outdir is a required parameter.")

#Import batch ids
batch_ids = list()
gene_count = list()
batch_file = open(args.geneBatches)
for line in batch_file:
	line = line.rstrip()
	fields = line.split("\t")
	batch_id = fields[0]
	batch_ids.append(batch_id)

	#Filter gene_coords BED file to only contain batch genes
	#Create dictionalry of gene ids
	gene_ids = fields[1].split(";")
	gene_count.append(len(gene_ids))
#print(batch_ids)
#print(gene_count)

#Iterate over batches and merge the results
read_first_file = False
#Open the output file
output_file = os.path.join(args.outdir, args.outprefix + args.suffix)
print(output_file)
output_file_handle = gzip.open(output_file, "w")

#Iterate through all batches
for batch_id in batch_ids:
	file_name = batch_id + "." + args.outprefix + args.suffix
	batch_out_path = os.path.join(args.outdir, batch_id, file_name)
	print(batch_out_path)
	batch_out_file = gzip.open(batch_out_path)

	#Skip the first line for all files except the first one
	if read_first_file:
		batch_out_file.readline()
	for line in batch_out_file:
		output_file_handle.write(line)
	batch_out_file.close()
	read_first_file = True

output_file_handle.close()