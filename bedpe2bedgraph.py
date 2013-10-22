import sys;

bedpe = open(sys.argv[1])
for line in bedpe:
	line = line.rstrip()
	fields = line.split("\t")
	#Check for chimereas
	if fields[0] == fields[3]:
		if fields[0] != "." and fields[0][0] != "H":
			fragment_length = int(fields[5]) - int(fields[1])
			if fragment_length < 1000:
				out = "\t".join([fields[0], fields[1], fields[5]])
				print(out)