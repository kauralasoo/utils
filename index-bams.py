import fileinput
import os
import sys
import argparse

parser = argparse.ArgumentParser(description = "Move BAMS from tophat2 folders to single folder and rename.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--bamdir", help = "Path to directory of bam files.", default = "bams_tophat2")
args = parser.parse_args()

for line in fileinput.input("-"):	
	line = line.rstrip()
	index_command = "samtools index " + os.path.join(args.bamdir, line)
	print(index_command)
	os.system(index_command)