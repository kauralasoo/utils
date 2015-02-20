import subprocess
import os
import argparse

parser = argparse.ArgumentParser(description = "For each sample find all the irods files that contain data from it.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--irodsList", help = "Path to file containing all irods sample names.")
args = parser.parse_args()

def stringToMetaDict(imeta_out):
	#Iterate thourg the text and extract key:value pairs.
	metadata = dict()
	attr = ""
	value = ""
	for line in imeta_out.split("\n"):
		line = line.rstrip()
		if line[0:9] == "attribute":
			fields = line.split("attribute: ")
			attr = fields[1]
		if line[0:5] == "value":
			fields = line.split("value: ")
			value = fields[1]
		if line[0:4] == "----":
			metadata[attr] = value
	return(metadata)

def buildIrodsPath(sample_id, input_format):
	#Build irods file path from irods sample id
	run_id = sample_id.split("_")[0]
	irods_path = os.path.join("/seq", run_id, sample_id + "." + input_format)
	return(irods_path)

#Fetch sample name for all files from iRODS
ids = open(args.irodsList)
sample_id_pairs = list()
for id in ids:
	id = id.rstrip()
	path = buildIrodsPath(id, "cram")
	imeta_cmd = "imeta ls -d " + path
	sample_meta = stringToMetaDict(subprocess.check_output(['bash','-c',imeta_cmd]))
	print(sample_meta)
	if "sample_public_name" in sample_meta:
		sample_id_pairs.append([id, sample_meta["sample_public_name"]])
	else:
		sample_id_pairs.append([id, sample_meta["sample"]])


#Match individual irods ids to sample ids
sample_dict = dict()
for pair in sample_id_pairs:
	sample_name = pair[1]
	file_name = pair[0]
	if sample_name in sample_dict:
		sample_dict[sample_name] = sample_dict[sample_name] + [file_name]
	else:
		sample_dict[sample_name] = [file_name]

#Print the file names for each sample id
for sample_name in sample_dict.keys():
	string = "\t".join([sample_name, ";".join(sample_dict[sample_name])])
	print(string)

