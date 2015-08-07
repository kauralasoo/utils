import sys
import os
import argparse
import fileinput

parser = argparse.ArgumentParser(description = "Submit jobs to the farm.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--jobname", help = "Name of the job")
parser.add_argument("--command", help = "Excact command to be submitted.")
parser.add_argument("--MEM", help = "Amount of memory required.")
parser.add_argument("--farmout", help = "Folder for FARM log files", default = "FarmOut")
parser.add_argument("--ncores", help = "Number of cores to use", default = "1")
parser.add_argument("--queue", help = "Queue for submitting the jobs into.", default = "normal")
args = parser.parse_args()

memory_string = ' -R"select[nfs_nobackup] rusage[mem=' + args.MEM +']" -M '+args.MEM
output_file = os.path.join(args.farmout, args.jobname + '.%J.txt')

for line in fileinput.input("-"):
	line = line.rstrip()
	command = "".join(["bsub -o ", output_file, " -q " + args.queue, " -n " + args.ncores, memory_string, " -J ", args.jobname, " \"echo '", line,"'", " | ", args.command, "\""])
	print(command) 
	os.system(command)

