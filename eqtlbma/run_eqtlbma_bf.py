import sys
import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Wrapper script to run eqtlbma_bf command.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the eqtlbma input files.")
parser.add_argument("--outdir", help = "Directory of the eqtlbma output files.")
parser.add_argument("--outprefix", help = "Prefix of the output files.")
parser.add_argument("--cis", help = "Width of the cis region.", default = "500000")
parser.add_argument("--error", help = "Model for the errors.", default = "mvlr")
parser.add_argument("--v", help = "Verbosity.", default = "3")
parser.add_argument("--bfs", help = "Which bayes factors to compute.", default = "all")
parser.add_argument("--gridL", help = "Path to the large grid.", default = "macrophage-gxe-study/data/eqtlbma/grid_phi2_oma2_general.txt")
parser.add_argument("--gridS", help = "Path to the small grid.", default = "macrophage-gxe-study/data/eqtlbma/grid_phi2_oma2_with-configs.txt")
parser.add_argument("--analys", help = "Type of analysis to perform.", default = "join")
parser.add_argument("--thread", help = "Number of threads to use.", default = 1)
parser.add_argument("--nperm", help = "Number of permutations to perform.")
parser.add_argument("--pbf", help = "which BF to use as the test statistic for the joint-analysis permutations.", default = "all")
parser.add_argument("--execute", help = "Execute the commands.", default = "True")
 --nperm 250 --pbf all -
args = parser.parse_args()

if args.indir == None:
	sys.exit("--indir is a required parameter.")
if args.outdir == None:
	sys.exit("--outdir is a required parameter.")
if args.outprefix == None:
	sys.exit("--outprefix is a required parameter.")

for line in fileinput.input("-"):
	line = line.rstrip()
	fields = line.split("\t")
	batch_id = fields[0]
	
	#Filter gene_coords BED file to only contain batch genes
	#Create dictionalry of gene ids
	gene_ids = fields[1].split(";")
	gene_dict = dict()
	for gene in gene_ids:
		gene_dict[gene] = 1

	#Construct file names
	geno_list = os.path.join(args.indir, "list.genotypes.txt")
	exp_list = os.path.join(args.indir, "list.expression.txt")
	covar_list = os.path.join(args.indir, "list.covariates.txt")
	snp_coords = os.path.join(args.indir, "snp_coords.bed.gz")
	gene_coords = os.path.join(args.indir, "gene_coords.bed")
	
	#Make output folders
	output_folder = os.path.join(args.outdir, batch_id)
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)
	gene_coords_batch = os.path.join(output_folder, batch_id + ".gene_coords.bed")
	output_file = os.path.join(output_folder, batch_id + "." + args.outprefix)

	#Create a custom gene coords bed file for each batch
	gene_coords_bed = open(gene_coords)
	gene_coords_batch_bed = open(gene_coords_batch, "w")
	for entry in gene_coords_bed:
		fields = entry.split("\t")
		if (fields[3] in gene_dict):
			gene_coords_batch_bed.write(entry)
	gene_coords_bed.close()
	gene_coords_batch_bed.close()

	#Construct eqtlbma command
	eqtlbma_command = " ".join(["eqtlbma_bf --geno", geno_list, "--exp", exp_list, "--covar", covar_list, "--scoord", snp_coords, "--gcoord", gene_coords_batch, "--anchor TSS --cis", args.cis, "--out", output_file, "--analys", args.analys, "--gridL", args.gridL, "--gridS", args.gridS, "--bfs", args.bfs, "--error", args.error, "-v", args.v, "--thread", args.thread])
	#Modify the command if doing permutations
	if args.nperm != None:
		eqtlbma_command  = " ".join(["eqtlbma_command", "--nperm", args.nperm, "--pbf", args.pbf, "--trick"])

	print(eqtlbma_command)
	
	#Execute
	if args.execute == "True":
		subprocess.call(['bash','-c',eqtlbma_command])
