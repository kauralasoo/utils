import sys
import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Remove duplicate reads and fragments from the BAM file.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input BAM files.")
parser.add_argument("--outdir", help = "Directory of the output BAM files.")
parser.add_argument("--insuffix", help = "Suffix of the input bam file.", default = ".reheadered.bam")
parser.add_argument("--outsuffix", help = "Suffix of the output bam file.", default = ".no_duplicates.bam")
parser.add_argument("--execute", help = "Execute the script", default = "False")
args = parser.parse_args()

#Construct file names
for line in fileinput.input("-"):
		sample_name = line.rstrip()
		path_in = os.path.join(args.indir, sample_name, sample_name + args.insuffix)
		path_out = os.path.join(args.outdir, sample_name, sample_name + args.outsuffix)
		metrics_file = os.path.join(args.outdir, sample_name, sample_name + ".MarkDuplicates.txt")
		picard_path = "/software/java/bin/java -jar -Xmx1800m /nfs/users/nfs_k/ka8/software/picard-tools-1.134/picard.jar"
		command = " ".join([picard_path, "MarkDuplicates", "I="+path_in, "O="+path_out , "REMOVE_DUPLICATES=true", "METRICS_FILE="+metrics_file])
		print(command)
		if args.execute == "True":
			subprocess.call(['bash','-c',command])