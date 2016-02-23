import sys
import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Use GATK ASEReadCounter to count allele-specific expression.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input BAM files.")
parser.add_argument("--outdir", help = "Directory of the output BAM files.")
parser.add_argument("--insuffix", help = "Suffix of the input bam file.", default = ".bam")
parser.add_argument("--outsuffix", help = "Suffix of the output ASE count file.", default = ".ASEcounts")
parser.add_argument("--reference", help = "Path to indexed reference FASTA file.")
parser.add_argument("--sites", help = "Path to the VCF file containing SNP coordinates.")
parser.add_argument("--execute", help = "Execute the script", default = "False")
parser.add_argument("--Xmx", help = "Memory allocated to the Java process.", default = "900m")
parser.add_argument("--java_path", help = "Path to the Java executable.", default = "/software/java/bin/java")
parser.add_argument("--gatk_path", help = "Path to the GATK executable.", default = "~/software/GenomeAnalysisTK.jar")
args = parser.parse_args()

#Construct file names
for line in fileinput.input("-"):
		sample_name = line.rstrip()
		path_in = os.path.join(args.indir, sample_name, sample_name + args.insuffix)
		path_out = os.path.join(args.outdir, sample_name, sample_name + args.outsuffix)
		gatk_path = " ".join([args.java_path, "-jar", "-Xmx"+args.Xmx, args.gatk_path, "-T ASEReadCounter"])
		#The -dt NONE flag disables downsampling in GATK
		flags = "-U ALLOW_N_CIGAR_READS -dt NONE --minMappingQuality 10 -rf MateSameStrand"
		command = " ".join([gatk_path, "-R", args.reference, "-I", path_in, "-o", path_out, "-sites", args.sites, flags])
		print(command)
		if args.execute == "True":
			subprocess.call(['bash','-c',command])
