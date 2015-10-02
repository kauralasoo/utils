import os
import sys
import argparse
import fileinput

parser = argparse.ArgumentParser(description = "Compress MISO results reduce the number of files.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--miso_folder", help = "Path to the folder of MISO results")
parser.add_argument("--tar_folder", help = "Path to the folder for the tar files.")
args = parser.parse_args()

for line in fileinput.input("-"):
	line = line.rstrip()
	miso_path = os.path.join(args.miso_folder, line)
	tar_path = os.path.join(args.tar_folder, line + ".tar.gz")
	command = " ".join(["tar czf",tar_path, miso_path])
	print(command)
	os.system(command)