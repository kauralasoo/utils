#! /usr/bin/python2.7
import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Use skewer to trim adapters from ATAC-seq fastq files.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--fastqDirIn", help = "Directory of the input fastq files.")
parser.add_argument("--fastqDirOut", help = "Directory of the output fastq files.")
parser.add_argument("--atacPrimers", help = "Path to ATAC primers file (columns: name, sequence, reverse_complement).")
parser.add_argument("--sampleIndexMap", help = "Text file linking sample_ids to i5 and i7 tags names (columns: sample_name, i5_tag, i7_tag).")
parser.add_argument("--suffix", help = "suffix of the FASTQ file,", default = ".fastq.gz")
parser.add_argument("--outSuffix", help = "suffix of the output FASTQ file,", default = ".trimmed.fastq.gz")
parser.add_argument("--i5rc", help = "Use the reverse complement of the i5 sequence.", default = "True")
parser.add_argument("--i7rc", help = "Use the reverse complement of the i7 sequence,", default = "True")
args = parser.parse_args()

#Import primer sequences into dictionary
primer_dict = dict()
primer_file = open(args.atacPrimers, "r")
for line in primer_file:
	line = line.rstrip()
	fields = line.split("\t")
	if fields[0] != "name":
		primer_dict[fields[0]] = fields[1:3]

#Import sample tag names into dictionary
sample_index_dict = dict()
sample_file = open(args.sampleIndexMap, "r")
for line in sample_file:
	line = line.rstrip()
	fields = line.split("\t")
	if fields[0] != "sample_id":
		sample_index_dict[fields[0]] = fields[1:3]

for line in fileinput.input("-"):
	sample_id = line.rstrip()
	print(sample_id)
	#Find the correct indexes for each sample
	indexes = sample_index_dict[sample_id]
	if args.i5rc == "True":
		i5_rc = primer_dict[indexes[0]][1]
	else:
		i5_rc = primer_dict[indexes[0]][0]
	if args.i7rc == "True":
		i7_rc = primer_dict[indexes[1]][1]
	else:
		i7_rc = primer_dict[indexes[1]][0]

	#Construct full i5 and i7 primer sequences
	i7_primer = "CTGTCTCTTATACACATCTCCGAGCCCACGAGAC" + i7_rc + "ATCTCGTATGCCGTCTTCTGCTTG"
	i5_primer = "CTGTCTCTTATACACATCTGACGCTGCCGACGA" + i5_rc + "GTGTAGATCTCGGTGGTCGCCGTATCATT"

	#Construct skewer command
	fq1 = os.path.join(args.fastqDirIn, sample_id + ".1" + args.suffix)
	fq2 = os.path.join(args.fastqDirIn, sample_id + ".2" + args.suffix)
	output_prefix = os.path.join(args.fastqDirOut, sample_id)
	skewer_command = " ".join(["skewer -x", i7_primer, "-y", i5_primer, "-m pe", fq1, fq2, "-z -o", output_prefix])
	print(skewer_command)
	subprocess.call(['bash','-c',skewer_command])

	#Rename trimmed fastq files
	fq1_out = output_prefix + "-trimmed-pair1.fastq.gz"
	fq2_out = output_prefix + "-trimmed-pair2.fastq.gz"
	fq1_out_mv = output_prefix + ".1" + args.outSuffix
	fq2_out_mv = output_prefix + ".2" + args.outSuffix
	mv_command_1 = " ".join(["mv", fq1_out, fq1_out_mv])
	mv_command_2 = " ".join(["mv", fq2_out, fq2_out_mv])
	print(mv_command_1)
	print(mv_command_2)
	subprocess.call(['bash','-c',mv_command_1])
	subprocess.call(['bash','-c',mv_command_2])

