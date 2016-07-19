import sys
import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Convert a BAM file to a text file of junctions suitable for LeafCutter", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input BAM files.")
parser.add_argument("--outdir", help = "Directory of the output junction files.")
parser.add_argument("--leafCutterDir", help = "Directory of the LeafCutter software.", default = "~/software/leafcutter/")
parser.add_argument("--insuffix", help = "Suffix of the input BAM file.", default = ".bam")
parser.add_argument("--outsuffix", help = "Suffix of the output junctions file.", default = ".junc")
parser.add_argument("--execute", help = "Execute the script", default = "False")
args = parser.parse_args()

#Construct file names
for line in fileinput.input("-"):
		sample_name = line.rstrip()
		
		#Set up file paths
		bam_file = os.path.join(args.indir, sample_name, sample_name + args.insuffix)
		bed_file = os.path.join(args.outdir, sample_name, sample_name + ".bed")
		junctions_file = os.path.join(args.outdir, sample_name, sample_name + args.outsuffix)

		#Set up tool paths
		cs_script = os.path.join(args.leafCutterDir, "scripts/filter_cs.py")
		sam2bed_script = os.path.join(args.leafCutterDir, "scripts/sam2bed.pl")
		bed2junc_script = os.path.join(args.leafCutterDir, "scripts/bed2junc.pl")

		#Construct commands
		bam2bed_command = " ".join(["samtools view", bam_file, "| python", cs_script, "|", sam2bed_script, "--use-RNA-strand -", bed_file])
		bed2junc_command = " ".join([bed2junc_script, bed_file, junctions_file])
		remove_bed_command = " ".join(["rm", bed_file])

		#Print and execute
		print(bam2bed_command)
		print(bed2junc_command)
		if args.execute == "True":
			subprocess.call(['bash','-c',bam2bed_command])
			subprocess.call(['bash','-c',bed2junc_command])
			subprocess.call(['bash','-c',remove_bed_command])

