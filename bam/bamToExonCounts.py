import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Count the number of fragments in BAM file that overlap exons/introns in GTF file", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--sampleDir", help = "Path to sample directory.")
parser.add_argument("--outDir", help = "Only needed if different from sampleDir.", default = "sampleDir")
parser.add_argument("--bamSuffix", help = "Full suffix of the bam file.", default = ".Aligned.out.bam")
parser.add_argument("--countsSuffix", help = "Suffix of the counts file.", default = ".counts.txt")
parser.add_argument("--gtf", help = "Path to gene annotations in GTF format")
parser.add_argument("--execute", help = "If True then executes the command, otherwise just prints it out.", default  = "True")
parser.add_argument("--strand", help = "0 (unstranded); 1 (stranded); 2(reversely stranded)", default = "0")
parser.add_argument("--multimapping", help = "Count multimapping reads.", default = "False")
parser.add_argument("--type", help = "Feature type in the GTF file (intron or exon).", default = "exon")
parser.add_argument("--subdir", help = "Is each sample in a subdirectory", default = "True")

args = parser.parse_args()

#Iterate over all ids
for line in fileinput.input("-"):
	line = line.rstrip()
	#Set output directory
	if args.outDir == "sampleDir":
		outdirectory = args.sampleDir
	else:
		outdirectory = args.outDir
	#Are subdirs used or not?
	if args.subdir == "True":
		bam_file = os.path.join(args.sampleDir, line, line + args.bamSuffix)
		count_file = os.path.join(outdirectory, line, line + args.countsSuffix)
	else:
		bam_file = os.path.join(args.sampleDir, line + args.bamSuffix)
		count_file = os.path.join(outdirectory, line + args.countsSuffix)
	
	featureCounts_command = " ".join(["featureCounts -a", args.gtf, "-o", count_file, "-f -C -D 2000 -d 25 --read2pos 5", "-s", args.strand, "-t", args.type])
	if(args.multimapping == "True"):
		featureCounts_command = featureCounts_command + " -M"
	command = " ".join([featureCounts_command, bam_file])
	print(command)
	if (args.execute == "True"):
		subprocess.call(['bash','-c',command])
