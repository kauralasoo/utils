import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Count the number of fragments in BAM file that overlap features in GTF file", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--sampleDir", help = "Path to sample directory.")
parser.add_argument("--bamSuffix", help = "Full suffix of the bam file.", default = ".Aligned.out.bam")
parser.add_argument("--countsSuffix", help = "Suffix of the counts file.", default = ".counts.txt")
parser.add_argument("--gtf", help = "Path to gene annotations in GTF format")
parser.add_argument("--execute", help = "If True then executes the command, otherwise just prints it out.", default  = "True")
parser.add_argument("--strand", help = "0 (unstranded); 1 (stranded); 2(reversely stranded)", default = "0")
parser.add_argument("--multimapping", help = "Count multimapping reads.", default = "False")
parser.add_argument("--unpaired", help = "BAM contains single-end reads.", default = "False")
parser.add_argument("--D", help = "Maximum insert size.", default = "2000")
parser.add_argument("--donotsort", help = "Do not sort the BAM file", default = "False")
parser.add_argument("--O", help = "Assign reads to all overlapping features.", default = "False")
parser.add_argument("--parameters", help = "Additional parameters passed on to featureCounts. These must be in single quotes and the first dash must be escaped with the \\ character, for example '\-f'.")
args = parser.parse_args()

#Iterate over all ids
for line in fileinput.input("-"):
	line = line.rstrip()
	bam_file = os.path.join(args.sampleDir, line, line + args.bamSuffix)
	count_file = os.path.join(args.sampleDir, line, line + args.countsSuffix)
	featureCounts_command = " ".join(["featureCounts -a", args.gtf, "-o", count_file, "-s", args.strand])
	if(args.multimapping == "True"):
		featureCounts_command = featureCounts_command + " -M"
	if(args.donotsort == "True"):
		featureCounts_command = featureCounts_command + " --donotsort"
	if(args.O == "True"):
		featureCounts_command = featureCounts_command + " -O"
	if(args.unpaired == "False"):
		featureCounts_command = " ".join([featureCounts_command, "-p -C -D", args.D, "-d 25"])
	#Add any additional parameters to RASQUAL
	if (args.parameters != None):
		params = args.parameters[1:]#Remove the first escape character
		featureCounts_command = " ".join([featureCounts_command, params])
	command = " ".join([featureCounts_command, bam_file])
	print(command)
	if (args.execute == "True"):
		subprocess.call(['bash','-c',command])
