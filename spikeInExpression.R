total_reads = c(139030806, 146832453)

#Load ERCC read counts
ercc_counts = read.table("Loven_2012/counts/ERCC92.counts")
ercc_reads = colSums(ercc_counts[,13:14])
ercc_lengths = ercc_counts[,3] / 1000
ercc_rpkm = ercc_counts[,c(13,14)]
rownames(ercc_rpkm) = as.vector(ercc_counts[,4])
ercc_rpkm = ercc_rpkm / ercc_lengths
ercc_rpkm = t(t(ercc_rpkm) / (total_reads*0.000001))


#Load ERCC reference values
reference = read.table("annotations/ERCC/ERCC_Controls_Analysis.txt", skip = 1)
rownames(reference) = reference[,2]
reference = reference[,c(4,5)]
reference = reference[rownames(ercc_rpkm),]

#Load Ensembl counts
ensembl_counts = read.table("Loven_2012/counts/Ensembl_69.counts")
ensembl_rpkm = ensembl_counts[,c(13,14)]
rownames(ensembl_rpkm) = as.vector(ensembl_counts[,4])

#Calculate RPKM values
length = unlist(lapply(strsplit(as.vector(ensembl_counts[,11]),","), function(x) sum(as.numeric(x))))/1000 
ensembl_rpkm = ensembl_rpkm/length
ensembl_rpkm = t(t(ensembl_rpkm) / ((total_reads - ercc_reads)*0.000001))

ensembl_present = ensembl_rpkm[apply(ensembl_rpkm,1, min) >= 1,]
ercc_present = ercc_rpkm[apply(ercc_rpkm,1, min) > 0,]

#Normalize RPKM values with LOESS
ercc_indexes = (nrow(all_rpkm)-nrow(ercc_present)+1):nrow(all_rpkm)
all_rpkm = rbind(ensembl_present, ercc_present)
normalized_rpkm = loess.normalize(all_rpkm, ercc_indexes, maxit = 10)

#Plot raw values
pdf("Loven_2012/results/spike-in_normalization.pdf")
ref = reference[rownames(ercc_present),]
plot(log(ref[,1],2), log(ercc_present[,1],2), xlab = "Log2 reference concentration", ylab = "Log2 expression", main = "Spike-in expression before normalization")
points(log(ref[,1],2), log(ercc_present[,2],2), col = "red")

#Plot normalized values
ercc_norm = normalized_rpkm[rownames(ercc_present),]
plot(log(ref[,1],2), log(ercc_norm[,1],2), xlab = "Log2 reference concentration", ylab = "Log2 expression", main = "Spike-in expression after normalization")
points(log(ref[,1],2), log(ercc_norm[,2],2), col = "red")

#Plot fold-change
ensembl_log = log(ensembl_present, 2)
norm_log = log(normalized_rpkm[1:nrow(ensembl_present),],2)
hist(ensembl_log[,2] - ensembl_log[,1], main = "Fold-change before LOESS normalization", breaks = 20)
hist(norm_log[,2] - norm_log[,1], main = "Fold-change after LOESS normalization", breaks = 20)
dev.off()
