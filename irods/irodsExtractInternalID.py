import subprocess
import os
import argparse

parser = argparse.ArgumentParser(description = "Extract Sanger internal ID for sample names list.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--sampleNames", help = "Path to the fail mapping sample names to lanelets.")
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

samples = open(args.sampleNames)

for line in samples:
	line = line.rstrip()
	fields = line.split("\t")
	sample_id = fields[0]
	lanelet_id = fields[1].split(";")[0]

	#Fetch data from irods
	path = buildIrodsPath(lanelet_id, "cram")
	imeta_cmd = "imeta ls -d " + path
	sample_meta = stringToMetaDict(subprocess.check_output(['bash','-c',imeta_cmd]))
	
	sample_id1 = ""
	sample_id2 = ""
	if "sample_id" in sample_meta:
		 sample_id1 = sample_meta["sample_id"]
	if "sample" in sample_meta:
		sample_id2 = sample_meta["sample"]
	result = "\t".join([sample_id, lanelet_id, sample_id1, sample_id2])
	print result

