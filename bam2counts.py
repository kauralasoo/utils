import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Count the number of fragments in BAM file that overlap features in GTF file", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--sampleDir", help = "Path to sample directory.")
parser.add_argument("--bamSuffix", help = "Full suffix of the bam file.", default = ".Aligned.out.bam")
parser.add_argument("--gtf", help = "Path to gene annotations in GTF format")
parser.add_argument("--execute", help = "If True then executes the command, otherwise just prints it out.", default  = "True")
parser.add_argument("--strand", help = "0 (unstranded); 1 (stranded); 2(reversely stranded)", default = "0")
args = parser.parse_args()

#Iterate over all ids
for line in fileinput.input("-"):
	line = line.rstrip()
	bam_file = os.path.join(args.sampleDir, line, line + args.bamSuffix)
	count_file = os.path.join(args.sampleDir, line, line + ".counts.txt")
	command = " ".join(["featureCounts -a", args.gtf, "-o", count_file, "-p -C -D 2000 -d 25", "-s", args.strand, bam_file])
	print(command)
	if (args.execute == "True"):
		subprocess.call(['bash','-c',command])
	#for chrom in chrnames:
	#	annot_file = os.path.join(args.annotations, chrom + ".gz")
	#	command = " ".join(["tabix", tabix_file, chrom, "| /nfs/users/nfs_n/nk5/bin/countReadChrom", annot_file, "| gzip >>", count_file])
	#	print command
	#	os.system(command)
#tabix tbxs/10506_0#1.tbx.gz ERCC-00171 | /nfs/users/nfs_n/nk5/bin/countReadChrom ../../annotations/GRCh37/Ensembl_69/nk5/ERCC-00171.gz -exon | gzip > 1.gz