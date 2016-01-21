import sys
import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Merge results from individual RASQUAL batches into a single file. Only keep columns 1,2,3,4,7,8,9,11,12,13,14,15,17,18,23 from the original file.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--prefix", help = "Prefix of the rasqual output files.")
args = parser.parse_args()

#Construct input and output files
input_files = args.prefix + '.batch_*.txt'
output_file = args.prefix + '.txt'

command = " ".join(["cat", input_files, "| cut -f 1,2,3,4,7,8,9,11,12,13,14,15,17,18,23 > ", output_file])
print(command)
subprocess.call(['bash','-c',command])

