#! /usr/bin/python2.7
import os
import sys
import argparse

#Parse command line arguments
parser = argparse.ArgumentParser(description = "Align RNA-Seq reads to the reference genome using TopHat2.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("reads", nargs = "*", help = "Path to FASTQ files.")
parser.add_argument("--gtf", help = "GTF/GFF file for TopHat", 
	default = "/nfs/users/nfs_k/ka8/group-scratch/kaur/annotations/GRCh37/Ensembl_72/Homo_sapiens.GRCh37.72.gff")
parser.add_argument("--index", help = "Bowtie2 index location.", 
	default = "/nfs/users/nfs_k/ka8/group-scratch/kaur/annotations/GRCh37/bowtie2-index/GRCh37")
parser.add_argument("--MEM", help = "Memory requirements for farm (MB).", default = "4500")
parser.add_argument("--out", help = "TopHat2 output folder.", default = "./tophat_out")
parser.add_argument("--ncores", help = "Number of cores to use.", default = "1")
parser.add_argument("--txindex", help = "Path to transcriptome index")
parser.add_argument("--library", help = "library type for TopHat2.")
args = parser.parse_args()

#Set up TopHat arguments
tophat2_arguments = ["tophat2",
					"--no-coverage-search", 
					"--GTF " + args.gtf, 
					"-o " + args.out,
					"-p" + args.ncores]
#Add path to transcriptome index
if args.txindex:
	tophat2_arguments = tophat2_arguments + ["--transcriptome-index " + args.txindex]
if args.library:
	tophat2_arguments = tophat2_arguments + ["--library-type " + args.library]

tophat2_command = " ".join(tophat2_arguments + [args.index] + args.reads)
memory_string = "".join(['-R"select[mem>',args.MEM,'] rusage[mem=', args.MEM, ']" -M', args.MEM, " -G team170"])
bsub_command = " ".join(["bsub", memory_string, "-o "+args.out+"/farm-output.%J.txt", "-n " + args.ncores,  tophat2_command])
print(bsub_command)
os.system(bsub_command)



