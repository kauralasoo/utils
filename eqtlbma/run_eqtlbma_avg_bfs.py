import sys
import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Wrapper script to run eqtlbma_hm command and extract grid and config weights.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--workdir", help = "Directory of the eqtlbma results.")
parser.add_argument("--outprefix", help = "Prefix of the output files.")
parser.add_argument("--nsubgrp", help = "Number of subgroups.")
parser.add_argument("--dim", help = "Dimensions of the model.")
parser.add_argument("--execute", help = "Execute the commands.", default = "True")
parser.add_argument("--mode", help = "Mode of the eqtlbma_avg_bfs command [ebf, post]", default = "ebf")
parser.add_argument("--pi0", help = "Precalculated value for pi0, only requied for the post mode.")
args = parser.parse_args()

#Test for required parameters
if args.workdir == None:
	sys.exit("--workdir is a required parameter.")
if args.outprefix == None:
	sys.exit("--outprefix is a required parameter.")
if args.nsubgrp == None:
	sys.exit("--nsubgrp is a required parameter.")
if args.dim == None:
	sys.exit("--dim is a required parameter.")

#Set up files
input_file = os.path.join(args.workdir, args.outprefix + "_l10abfs_raw.txt.gz")
config_weights = os.path.join(args.workdir, args.outprefix + "_config_weights.txt")
grid_weights = os.path.join(args.workdir, args.outprefix + "_grid_weights.txt")
model_out_ebf = os.path.join(args.workdir, args.outprefix + "_avg_bfs_EBF.txt.gz")
model_out_post = os.path.join(args.workdir, args.outprefix + "_avg_bfs.txt.gz")

#Construct the command
eqtlbma_base_cmd = " ".join(["eqtlbma_avg_bfs --in", input_file, "--gwts", grid_weights, "--nsubgrp", args.nsubgrp, "--dim", args.dim, "--cwts", config_weights])

#Alter the command based on the mode
if args.mode == "ebf":
	eqtlbma_command = " ".join([eqtlbma_base_cmd, "--save bf --out", model_out_ebf])
elif args.mode == "post":
	if args.pi0 == None:
		sys.exit("--pi0 is a required parameter in 'post' mode.")
	eqtlbma_command = " ".join([eqtlbma_base_cmd, "--save bf+post --post a+b+c+d --bestdim --alldim --pi0", args.pi0, "--out", model_out_post])

#Run the command
print(eqtlbma_command)
if args.execute == "True":
	subprocess.call(['bash','-c',eqtlbma_command])
