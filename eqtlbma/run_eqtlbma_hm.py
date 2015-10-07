import sys
import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Wrapper script to run eqtlbma_hm command and extract grid and config weights.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--workdir", help = "Directory of the eqtlbma results.")
parser.add_argument("--outprefix", help = "Prefix of the output files.")
parser.add_argument("--ngrid", help = "Number of grid points.", default = "10")
parser.add_argument("--nsubgrp", help = "Number of subgroups.")
parser.add_argument("--dim", help = "Dimensions of the model.")
parser.add_argument("--execute", help = "Execute the commands.", default = "True")
parser.add_argument("--configs", help = "Subset of configurations to keep.")
parser.add_argument("--thread", help = "Number of threads to use.", default = "1")
args = parser.parse_args()

#Construct file names
input_file = os.path.join(args.workdir, args.outprefix + "_l10abfs_raw.txt.gz")
model_out = os.path.join(args.workdir, args.outprefix + "_hm.txt.gz")
config_weights = os.path.join(args.workdir, args.outprefix + "_config_weights.txt")
grid_weights = os.path.join(args.workdir, args.outprefix + "_grid_weights.txt")

#Set up the commands
eqtlbma_command = " ".join(["eqtlbma_hm --data", input_file, "--nsubgrp", args.nsubgrp, "--ngrid", args.ngrid, "--dim", args.dim, "--out", model_out, "--thread", args.thread])
#Select a subset of configurations to keep
if args.configs != None:
	eqtlbma_command = " ".join([eqtlbma_command, "--configs ",  "\""+args.configs+"\""])

config_command = " ".join(["zcat", model_out, '| grep "#config" | awk \'{split($1,a,"."); print a[2]"\\t"$2}\' > ', config_weights])
grid_command = " ".join(["zcat", model_out, '| grep "#grid" | cut -f2 >', grid_weights])

#Print the commands
print(eqtlbma_command)
print(config_command)
print(grid_command)

if args.execute == "True":
	subprocess.call(['bash','-c',eqtlbma_command])
	subprocess.call(['bash','-c',config_command])
	subprocess.call(['bash','-c',grid_command])
