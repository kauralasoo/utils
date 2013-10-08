#Count the number of bases mapping to each chromosome
import sys
import argparse
import fileinput
import os

parser = argparse.ArgumentParser(description = "Count the number of covered bases for each chr and change chr names.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--BGin", help = "Path to input BedGraph folder", default = "BedGraph")
parser.add_argument("--BGout", help = "Path to output BedGraph folder", default = "BedGraph/ucsc")
args = parser.parse_args()

#Iterate over all ids
for line in fileinput.input("-"):
	line = line.rstrip()
	bgin = os.path.join(args.BGin, line + ".bg")
	bgout = os.path.join(args.BGout, line + ".bg")

	#Count number of bases per chr
	bgfile = open(bgin)
	current_chr = "1"
	current_sum = 0
	count_list = list()
	for line in bgfile:
		line = line.rstrip()
		fields = line.split("\t")
		if fields[0] == current_chr:
			current_sum = current_sum + int(fields[3])
		else:
			count_list.append((current_chr, current_sum))
			current_chr = fields[0]
			current_sum = 0
	count_list.append((current_chr, current_sum))
	bgfile.close()

	#Write output
	bgoutfile = open(bgout, "w")

	#Print out total counts
	for element in count_list:
		bgoutfile.write("#" + "chr" + element[0] + ":" + str(element[1]) + "\n")

	#Print out the BedGraph file again 
	bg = open(bgin)
	for line in bg:
		bgoutfile.write("chr" + line)
	bgoutfile.close()

	#Zip and index
	os.system("bgzip -f " + bgout)
	os.system("tabix -s 1 -b 2 -e 3 " + bgout + ".gz")
