import os
import sys
import argparse
import fileinput

parser = argparse.ArgumentParser(description = "Count the number of fragments in BAM file that overlap features in GTF file", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--bams", help = "Path to BAM files", default = "bams_tophat2")
parser.add_argument("--counts", help = "Path to count files", default = "counts")
parser.add_argument("--gtf", help = "Path to gene annotations in GTF format", 
	default = "/nfs/users/nfs_k/ka8/group-scratch/kaur/annotations/GRCh37/Ensembl_72/Homo_sapiens.GRCh37.72.ERCC92.gtf")
parser.add_argument("--execute", help = "If True then executes the command, otherwise just prints it out.", default  = "True")
parser.add_argument("--strand", help = "0 (unstranded); 1 (stranded); 2(reversely stranded)", default = "0")
args = parser.parse_args()

#Iterate over all ids
for line in fileinput.input("-"):
	line = line.rstrip()
	bam_file = os.path.join(args.bams, line + ".bam")
	count_file = os.path.join(args.counts, line + ".txt")
	command = " ".join(["featureCounts -a", args.gtf, "-i", bam_file, "-o", count_file, "-b -p -C", "-s", args.strand])
	print(command)
	if (args.execute == "True"):
		os.system(command)
	#for chrom in chrnames:
	#	annot_file = os.path.join(args.annotations, chrom + ".gz")
	#	command = " ".join(["tabix", tabix_file, chrom, "| /nfs/users/nfs_n/nk5/bin/countReadChrom", annot_file, "| gzip >>", count_file])
	#	print command
	#	os.system(command)
#tabix tbxs/10506_0#1.tbx.gz ERCC-00171 | /nfs/users/nfs_n/nk5/bin/countReadChrom ../../annotations/GRCh37/Ensembl_69/nk5/ERCC-00171.gz -exon | gzip > 1.gz