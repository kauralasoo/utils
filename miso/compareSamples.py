import os
import sys
import argparse
import fileinput

parser = argparse.ArgumentParser(description = "Compress MISO results reduce the number of files.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--temp", help = "Temporary folder to store MISO results.")
parser.add_argument("--tar_folder", help = "Path to the folder for the tar files.")
parser.add_argument("--comparisons", help = "Path to comparisons text file.")
parser.add_argument("--output", help = "Path to MISO output files.")
args = parser.parse_args()

comp = open(args.comparisons)
for line in comp:
	line = line.rstrip()
	samples = line.split("\t")
	print(samples)

	#extract TARs
	tar1 = os.path.join(args.tar_folder, samples[0] +".tar.gz")
	tar2 = os.path.join(args.tar_folder, samples[1] +".tar.gz")
	untar1 = " ".join(["tar xzf ", tar1, "-C", args.temp])
	untar2 = " ".join(["tar xzf ", tar2, "-C", args.temp])
	print("Extracting archives ...")
	#os.system(untar1)
	#os.system(untar2)

	#Perform MISO comparison
	print("Comparing samples ...")
	sample1_dir = os.path.join(args.temp, samples[0])
	sample2_dir = os.path.join(args.temp, samples[1])
	miso_script = "python ~/software/miso/misopy/run_miso.py --compare-samples"
	command = " ".join([miso_script, sample1_dir, sample2_dir, args.output, "--comparison-labels", samples[0], samples[1]])
	os.system(command)

	#Create a transcript-centric view of the results
	comparison = samples[0] + "_vs_" + samples[1] 
	in_file_name = comparison + ".miso_bf"
	out_file_name = comparison+ ".miso_tx_bf"
	in_file_path = os.path.join(args.output, comparison, "bayes-factors", in_file_name)
	out_file_path = os.path.join(args.output, comparison, "bayes-factors", out_file_name)
	script = "python ~/software/utils/miso/gene2transcript.py"
	command2 = " ".join([script, in_file_path, ">", out_file_path])
	print(command2)
	os.system(command2)

	#Clean up temp
	print("Cleaning up ....")
	os.system("rm -r " + sample1_dir)
	os.system("rm -r " + sample2_dir)

