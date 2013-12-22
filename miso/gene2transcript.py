import sys

def extractIsoformNames(isoform_string):
	isoform_ids = list()
	isoforms = isoform_string.split(",")
	for isoform in isoforms:
		exons = isoform.split("_")
		ids = exons[0].split(":")
		isoform_id = ids[1]
		isoform_ids.append(isoform_id)
	return(isoform_ids)

def convertNumberString(number_string, n_isoforms):
	numbers = list()
	if n_isoforms == 2:
		numbers.append(number_string)
		numbers.append(str(1-float(number_string)))
	else:
		numbers = number_string.split(",")
	return(numbers)

def extractDiff(number_string, n_isoforms):
	numbers = list()
	if n_isoforms == 2:
		numbers.append(number_string)
		numbers.append(str(-1*float(number_string)))
	else:
		numbers = number_string.split(",")
	return(numbers)

def extractBF(number_string, n_isoforms):
	numbers = list()
	if n_isoforms == 2:
		numbers.append(number_string)
		numbers.append(number_string)
	else:
		numbers = number_string.split(",")
	return(numbers)

def extractReadsAssigned(reads_string):
	reads_list = list()
	reads = reads_string.split(",")
	for read in reads:
		reads_list.append(read.split(":")[1])
	return(reads_list)

file = open(sys.argv[1])
#Read and print header
header = file.readline()
header = header.split("\t")
print("\t".join(["gene_id", "transcript_id"] + header[1:9] + ["sample1_reads","sample2_reads", "transcript_number", "n_transcripts"]))

for line in file:
	line = line.rstrip()
	fields = line.split("\t")
	
	#Extract all individual parameters
	gene_id = fields[0]
	sample1_reads = extractReadsAssigned(fields[11]) #Extract number of assigned reads in sample 1
	sample2_reads = extractReadsAssigned(fields[13]) #Extract number of assigned reads in sample 2
	isoform_ids = extractIsoformNames(fields[9]) #Add isoform ids
	gene_ids = [gene_id]*len(isoform_ids) #Multiply gene ids
	statistics = map((lambda x: convertNumberString(x, len(isoform_ids)) ), fields[1:7]) #Add estimates and CIs
	diff = extractDiff(fields[7],len(isoform_ids)) #Add diff
	bayes_factors = extractBF(fields[8],len(isoform_ids)) #Add bayes factor
	transcript_number = map(str, range(1,len(isoform_ids)+1)) #Add Tx sequence number
	n_transcripts = [str(len(isoform_ids))]*len(isoform_ids) #Add total number of txs

	#Combine values and print the result
	values = [gene_ids, isoform_ids] + statistics + [diff, bayes_factors, sample1_reads, sample2_reads, transcript_number, n_transcripts]
	lines = map(list, zip(*values)) #Transpose list
	for line in lines:
		print "\t".join(line)
