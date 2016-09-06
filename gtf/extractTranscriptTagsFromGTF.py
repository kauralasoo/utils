import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Extract transcript tags from GTF file.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--GTF", help = "Path to the GTF file.")
args = parser.parse_args()

file_handle = open(args.GTF)
for line in file_handle:
	line = line.rstrip()
	#Remove headers
	if (line[0:2] == "#!"):
		pass
	else:
		fields = line.split("\t")
		if (fields[2] == "transcript"):
			tags = fields[8]
			tags = tags.rstrip('";')
			tag_fields = tags.split('"; ')

			#Construct tag pairs
			tag_pairs = list()
			for tag_field in tag_fields:
				tag_pairs.append(tag_field.split(' "'))

			#Iterate over pairs to extract tx_id and tags
			true_tags = list()
			transcript_id = ""
			for tag_pair in tag_pairs:
				if(tag_pair[0] == "transcript_id"):
					transcript_id = tag_pair[1]
				if(tag_pair[0] == "tag"):
					true_tags.append(tag_pair[1])
			if len(true_tags) > 0:
				print("\t".join([transcript_id, ";".join(true_tags)]))

