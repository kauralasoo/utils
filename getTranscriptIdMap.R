library(GenomicFeatures)

#Extract specific version of Ensembl
#txdb74 = makeTranscriptDbFromBiomart(biomart = "ENSEMBL_MART_ENSEMBL", dataset = "hsapiens_gene_ensembl", host="dec2013.archive.ensembl.org")

#Load txdv from disk
txdb = loadDb("../../annotations/GRCh37/Ensembl_74/Homo_sapiens.GRCh37.74.TranscriptDb.db")
genes = genes(txdb)
gene_ids = unlist(genes$gene_id)
tx_ids = select(txdb, keys = gene_ids, columns = c("GENEID","TXNAME"), keytype = "GENEID")
colnames(tx_ids) = c("gene_id", "transcript_id")
write.table(tx_ids, "../../annotations/GRCh37/Ensembl_74/Homo_sapiens.GRCh37.74.gene_tx_ids.txt", sep = "\t", quote = FALSE, row.names = FALSE)

