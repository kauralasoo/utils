import os
import argparse

parser = argparse.ArgumentParser(description = "Fetch BAM files from IRODS.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--runid", help = "Run ID in the IRODS database.")
parser.add_argument("--laneids", help = "Comma-separted list of lane ids")
parser.add_argument("--sampleids", help = "Comma-separated list of sample ids")
parser.add_argument("--dir", help = "Directory to store the BAM files.")
args = parser.parse_args()

def CreateSampleIds(runid, lanes, samples):
	"""Construct sample IDs for IRODS"""
	lanes = map(int,lanes.split(","))
	samples = map(int,samples.split(","))

	ids = list()
	#Iterate over lanes
	for lane in lanes:
		#Iterate over samples
		for sample in samples:
			sample_id = args.runid + "_" + str(lane) + "#" + str(sample)
			ids.append(sample_id)
	return(ids)

#Construct names for BAMs
ids = CreateSampleIds(args.runid, args.laneids, args.sampleids)
path = "/".join(["/seq", args.runid, ""])
bams = [path + id + ".bam" for id in ids]

#Download all BAM files
for bam in bams:
	command = " ".join(["iget", bam, args.dir])
	print(command)
	os.system(command)

