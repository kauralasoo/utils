#! /usr/bin/python2.7
import os
import sys
import argparse
import fileinput

parser = argparse.ArgumentParser(description = "Convert BAM files to Tabix files", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--chrnames", help = "Path to file containing chromosome names", 
	default = "/nfs/users/nfs_k/ka8/group-scratch/kaur/annotations/GRCh37/bowtie2-index/chromosome_names.txt")
parser.add_argument("--bams", help = "Path to indexed BAM files", default = "bams_tophat2")
parser.add_argument("--tbxs", help = "Path to TABIX files", default = "tbxs")
args = parser.parse_args()

#Read chromosome names from disk
chrnames_file = open(args.chrnames)
chrnames = chrnames_file.readlines()
chrnames = [chr.rstrip() for chr in chrnames]

#Iterate over sample ids
for line in fileinput.input("-"):
	line = line.rstrip()
	bam_file = os.path.join(args.bams, line + ".bam")
	tbx_file = os.path.join(args.tbxs, line + ".tbx")
	print bam_file
	print tbx_file
	#Delete exsisting files
	os.system("rm " + tbx_file)
	os.system("rm " + tbx_file +".gz")
	os.system("rm " + tbx_file +".gz.tbi")

	#Iterate over chromosomes
	for chr in chrnames:
		#Create Tabix file
		qc_command = "| /nfs/users/nfs_n/nk5/Project/C/qcFilterBam/qcFilterBam stdin -skipMissing=F -maxMismatch=3 -maxGapOpen=0 -maxBestHit=1 -minQual=10 -minInsert=76 -maxInsert=4349516 -bowtie | sort -k 2,2n"
		command = " ".join(["samtools view -F 0x0100", bam_file, chr, "| awk '$7==\"=\"{print}' | sort -k 1", qc_command, " >>", tbx_file])
		print(command)
		os.system(command)

	#Zip and index
	os.system("bgzip " + tbx_file)
	os.system("tabix -f -s 1 -b 2 -e 3 " + tbx_file + ".gz")
