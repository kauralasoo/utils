import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Fetch BAM files from IRODS.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--dir", help = "Directory to store the BAM files.")
parser.add_argument("--suffix", help = "Suffix of the file in irods.")

args = parser.parse_args()

def buildIrodsPath(sample_id, input_format):
	#Build irods file path from irods sample id
	run_id = sample_id.split("_")[0]
	irods_path = os.path.join("/seq", run_id, sample_id + input_format)
	return(irods_path)

for line in fileinput.input("-"):
	id = line.rstrip()
	irods_path = buildIrodsPath(id, args.suffix)
	command = " ".join(["iget", irods_path, args.dir])
	print(command)
	subprocess.call(['bash','-c',command])


