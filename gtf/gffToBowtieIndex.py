import fileinput
import os
import argparse
import subprocess


parser = argparse.ArgumentParser(description = "Convert GFF3 file into bowtie index for mmseq.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--fasta", help = "Path to genome fasta file.")
parser.add_argument("--wd", help = "Path to working directory with GFF3 file.")

args = parser.parse_args()

for line in fileinput.input("-"):	
	line = line.rstrip()
	gff_file = os.path.join(args.wd, line + ".gff3")
	fa_file = os.path.join(args.wd, line + ".fa")

	#Convert gff to fasta
	gff_fasta_cmd = " ".join(["gffread -w", fa_file, "-g", args.fasta, gff_file])
	print(gff_fasta_cmd)
	subprocess.call(['bash','-c',gff_fasta_cmd])

	#Index the fasta file
	index_path = os.path.join(args.wd, line)
	index_cmd = " ".join(["bowtie-build --offrate 3", fa_file, index_path])
	print(index_cmd)
	subprocess.call(['bash','-c',index_cmd])
