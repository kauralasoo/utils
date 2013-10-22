import os
import sys
import argparse
import fileinput

parser = argparse.ArgumentParser(description = "Caclulcate the meand and SD of insert size of RNA-Seq library.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--bams", help = "Path to BAM files", default = "bams_tophat2")
parser.add_argument("--output", help = "Path to output folder", default = "miso/insert-dist/")
parser.add_argument("--gtf", help = "Path to long exons in GFF format", default = "miso/long_exons/Homo_sapiens.GRCh37.72.min_1000.const_exons.gff")
parser.add_argument("--execute", help = "If True then executes the command, otherwise just prints it out.", default  = "True")
args = parser.parse_args()

for line in fileinput.input("-"):
	line = line.rstrip()
	bam_file = os.path.join(args.bams, line + ".bam")
	command = " ".join(["python ~/software/miso/misopy/pe_utils.py --compute-insert-len", bam_file, args.gtf, "--output-dir", args.output])
	print(command)
	if (args.execute == "True"):
		os.system(command)

