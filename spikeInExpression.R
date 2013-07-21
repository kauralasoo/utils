counts = read.table("Loven_2012/counts/ERCC92.counts")
lengths = counts[,3]
values = counts[,c(13,14)]

rownames(values) = as.vector(counts[,4])
values = values / lengths

 reference = read.table("annotations/ERCC/ERCC_Controls_Analysis.txt", skip = 1)
 rownames(reference) = reference[,2]
reference = reference[,c(4,5)]


