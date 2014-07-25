import os
import argparse

parser = argparse.ArgumentParser(description = "Fetch BAM files from IRODS.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--runid", help = "Run ID in the IRODS database.")
parser.add_argument("--laneids", help = "Number of lanes")
parser.add_argument("--sampleids", help = "Number of samples")
parser.add_argument("--indir", help = "Directory of the input BAM files")
parser.add_argument("--outdir", help = "Directory of the output BAM files")

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
lanes = args.laneids.split(",")
ids_per_lane = list()
for lane in lanes:
	ids = CreateSampleIds(args.runid, lane, args.sampleids)
	ids = [args.indir + "/" + id + ".bam" for id in ids]
	ids_per_lane.append(ids)

#Transpose list
ids_per_sample = map(list, zip(*ids_per_lane))

#Construct names for output bams
out_bams = CreateSampleIds(args.runid, "0", args.sampleids)
out_bams = [args.outdir + "/" + id + ".bam" for id in out_bams]

#Merge bams
for (i, j) in zip(ids_per_sample, out_bams):
	command = " ".join(["samtools merge"] + [j] + i)
	print(command)
	os.system(command)
