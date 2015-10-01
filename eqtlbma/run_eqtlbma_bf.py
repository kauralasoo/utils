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
parser.add_argument("--gcoord", help = "Path to text file with gene coordinates.")
parser.add_argument("--execute", help = "Execute the commands.", default = "True")
args = parser.parse_args()

#Check that none of the required arguments is empty
if args.gcoord == None:
	sys.exit("--gcoord is a required parameter.")

#Construct file names
geno_list = os.path.join(args.indir, "list.genotypes.txt")
exp_list = os.path.join(args.indir, "list.expression.txt")
covar_list = os.path.join(args.indir, "list.covariates.txt")
snp_coords = os.path.join(args.indir, "snp_coords.bed.gz")
gene_coords = args.gcoord
output_file = os.path.join(args.outdir, args.outprefix)

#Construct eqtlbma command
eqtlbma_command = " ".join(["eqtlbma_bf --geno", geno_list, "--exp", exp_list, "--covar", covar_list, "--scoord", snp_coords, "--gcoord", gene_coords, "--anchor TSS --cis", args.cis, "--out", output_file, "--analys", args.analys, "--gridL", args.gridL, "--gridS", args.gridS, "--bfs", args.bfs, "--error", args.error, "-v", args.v])
print(eqtlbma_command)

if args.execute == "True":
	subprocess.call(['bash','-c',eqtlbma_command])
