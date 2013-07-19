#! /usr/bin/python2.7
import os
import sys, getopt
import argparse

#Parse command line arguments
parser = argparse.ArgumentParser(description = "Align RNA-Seq reads to the reference genome using TopHat2.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("reads", nargs = "*", help = "Path to FASTQ files.")
parser.add_argument("--gtf", help = "GTF/GFF file for TopHat", 
	default = "/nfs/teams/team170/Ensembl/Homo_sapiens.GRCh37.69.gtf")
parser.add_argument("--index", help = "Bowtie2 index location.", 
	default = "/nfs/users/nfs_k/ka8/group-scratch/kaur/annotations/GRCh37/bowtie2-index/GRCh37")
parser.add_argument("--MEM", help = "Memory requirements for farm (MB).", default = "4500")
parser.add_argument("--out", help = "TopHat2 output folder.", default = "./tophat_out")
parser.add_argument("--ncores", help = "Number of cores to use.", default = "1")
args = parser.parse_args()

#"--GTF " + args.gtf, 
tophat2_command = " ".join(["tophat2", "--no-coverage-search","--GTF " + args.gtf,"-o " + args.out, "-p" + args.ncores, args.index] + args.reads)
memory_string = "".join(['-R"select[mem>',args.MEM,'] rusage[mem=', args.MEM, ']" -M', args.MEM, " -G team170"])
bsub_command = " ".join(["bsub", memory_string, "-o "+args.out+"/farm-output.%J.txt", "-n " + args.ncores,  tophat2_command])
print(bsub_command)
os.system(bsub_command)



