#! /usr/bin/python2.7
import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Map reads to transcript sets using bam2hits.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--fasta", help = "Path to the transcriptome FASTA file.")
parser.add_argument("--output", help = "Path to output folder.")
#parser.add_argument("--ncores", help = "Number of cores to use.", default = "1")
parser.add_argument("--bams", help = "Path to the bams folder.")
parser.add_argument("--gffread_fasta", help = "TRUE if the fasta file was created with the gffread utility.", default = "FALSE")
args = parser.parse_args()

for line in fileinput.input("-"):
	line = line.rstrip()
	bam_file = os.path.join(args.bams, line + ".bam")
	hits_file = os.path.join(args.output, line + ".hits")
	bam2hits = "bam2hits"
	if (args.gffread_fasta == "True"):
		bam2hits = 'bam2hits -m "(\S+).*gene=(\S+).*" 1 2'
	command = " ".join([bam2hits, args.fasta, bam_file, ">", hits_file])
	print(command)
	subprocess.call(['bash','-c',command])

#bam2hits ../../annotations/GRCh37/Ensembl_74/transcripts/Homo_sapiens.GRCh37.74.ref_transcripts.fa mmseq/bams/B1_ctrl.bam > mmseq/results/B1_ctrl.hits