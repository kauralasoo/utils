import subprocess
import os
import argparse

parser = argparse.ArgumentParser(description = "Fetch the list of all files associated with a study in irods.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--studyName", help = "Name of the irods study.")
args = parser.parse_args()

def stringToObjects(imeta_out):
	#Iterate thourg the text and extract key:value pairs.
	objects = list()
	for line in imeta_out.split("\n"):
		line = line.rstrip()
		if line[0:7] == "dataObj":
			fields = line.split("dataObj: ")
			objects.append(fields[1])
	return(objects)

#Extract object list from imeta output
imeta_cmd = "".join(["imeta qu -z seq -d study = '", args.studyName,"' and target = 1 and manual_qc = 1"])
meta_strings = subprocess.check_output(['bash','-c',imeta_cmd])
objects = stringToObjects(meta_strings)
for obj in objects:
	print obj

