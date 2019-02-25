import fileinput

stream = fileinput.input("-")
#Skip first line
stream.readline()
for line in stream:
    line = line.rstrip()
    fields = line.split("\t")
    variant_id = "_".join([fields[1], fields[2], fields[3]])
    output_bed = "\t".join([fields[1], fields[2], fields[2], variant_id])
    print(output_bed)