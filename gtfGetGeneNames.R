library(refGenome)

ensg <- ensemblGenome()
read.gtf(ensg, "../../annotations/GRCh37/Ensembl_74//Homo_sapiens.GRCh37.74.gtf")
moveAttributes(ensg,c("gene_name"))
moveAttributes(ensg,c("transcript_name"))
annotations = extractSeqids(ensg,"*")
gene_id_name_map = genes[,c("gene_id", "gene_name")]

