import os
import sys
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Combine intron and exon counts into intron retention events.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--sampleDir", help = "Path to sample directory.")
parser.add_argument("--intronCountSuffix", help = "Full suffix of the bam file.", default = ".intron_counts.txt")
parser.add_argument("--exonCountSuffix", help = "Suffix of the counts file.", default = ".exon_counts.txt")
parser.add_argument("--eventSuffix", help = "Suffix of the intron retention event file.", default = ".intron_events.txt")
parser.add_argument("--intronGFF", help = "Path to intron annotations in GFF3 format.")
parser.add_argument("--exonGFF", help = "Patho to exon annotations in GFF3 format.")
parser.add_argument("--subdir", help = "Is each sample in a subdirectory?", default = "True")
args = parser.parse_args()

def loadFeatureIDs(feature_file, feature_type):
	feature_list = list()
	file_gff = open(feature_file)
	for line in file_gff:
		line = line.rstrip()
		if line[0] != "#":
			fields = line.split("\t")
			if fields[2] == feature_type:
				feature_id = fields[8].split("ID=")[1]
				feature_list.append(feature_id)
	return(feature_list)

#Load intron and exon names from disk
intron_list = loadFeatureIDs(args.intronGFF, "intron")
exon_list = loadFeatureIDs(args.exonGFF, "exon")

#Iterate over sample ids and construct file names
for sample_id in fileinput.input("-"):
	sample_id = sample_id.rstrip()
	#Are samples stored in a subdirectory?
	if args.subdir == "True":
		exon_count_file = os.path.join(args.sampleDir, sample_id, sample_id + args.exonCountSuffix)
		intron_count_file = os.path.join(args.sampleDir, sample_id, sample_id + args.intronCountSuffix)
		intron_event_file = os.path.join(args.sampleDir, sample_id, sample_id + args.eventSuffix)
	else:
		exon_count_file = os.path.join(args.sampleDir, sample_id + args.exonCountSuffix)
		intron_count_file = os.path.join(args.sampleDir, sample_id + args.intronCountSuffix)
		intron_event_file = os.path.join(args.sampleDir, sample_id + args.eventSuffix)

	#Load exon counts into a dictionary
	exon_counts = dict()
	counter = 0
	exon_count_handle = open(exon_count_file)
	for line in exon_count_handle:
		if line[0] == "#":
			continue
		line = line.rstrip()
		fields = line.split("\t")
		if fields[0] != "Geneid":
			exon_id = exon_list[counter]
			exon_counts[exon_id] = int(fields[6])
			counter = counter + 1
	exon_count_handle.close()

	#Iterate through intron counts and find corresponding exon counts
	counter = 0
	intron_count_handle = open(intron_count_file)
	intron_event_handle = open(intron_event_file, "w")
	for line in intron_count_handle:
		if line[0] == "#":
			continue
		line = line.rstrip()
		fields = line.split("\t")
		if fields[0] != "Geneid":
			intron_id = intron_list[counter]
			intron_fields = intron_id.split("_")
			intron_no = int(intron_fields[2])
			upstream_exon = "_".join([intron_fields[0],"exon", str(intron_no)])
			downstream_exon = "_".join([intron_fields[0],"exon", str(intron_no + 1)])
			#Find intron and exon counts
			i_counts = fields[6]
			e_counts = exon_counts[upstream_exon] + exon_counts[downstream_exon]
			output = "\t".join([fields[0], intron_id, i_counts + ","+str(e_counts)+"\n"])
			intron_event_handle.write(output)
			counter = counter + 1
	#Close the files
	intron_count_handle.close()
	intron_event_handle.close()
