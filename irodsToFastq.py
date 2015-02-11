#! /usr/bin/python2.7
# Script to fetch reads from irods and convert them to Fastq
import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Fetch sequencing reads from iRODS and convert them to fastq.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--output", help = "Path to output folder.")
parser.add_argument("--inputformat", help = "Specify which input format to use.", default = "cram")
parser.add_argument("--suffix", help = "Suffix of the FASTQ files", default = ".fastq.gz")

args = parser.parse_args()

for line in fileinput.input("-"):
	chunk_id = line.rstrip()
	run_id = chunk_id.split("_")[0]
	irods_path = os.path.join("/seq", run_id, chunk_id + "." + args.inputformat)
	biobambam_command = "/software/hpag/biobambam/latest/bin/bamtofastq exclude=SECONDARY,SUPPLEMENTARY,QCFAIL inputformat=" + args.inputformat
	output_file1 = os.path.join(args.output, chunk_id + ".1" +  args.suffix)
	output_file2 = os.path.join(args.output, chunk_id + ".2" + args.suffix)
	command = " ".join(["iget", irods_path, "-", "|", biobambam_command, "gz=1", "F="+output_file1, "F2="+output_file2])
	print(command)
	subprocess.call(['bash','-c',command])
