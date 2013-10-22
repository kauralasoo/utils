#Download Ensembl transcript annotations from biomaRt and apply sensible filters

#Load libraries
suppressPackageStartupMessages(library(optparse))
library("biomaRt")

#Parse options
option_list <- list(
make_option(c("-t", "--transcript-table"), type="character", default=NULL,
help="Path to the file storing the transcript table.", metavar = "path")
)
opt <- parse_args(OptionParser(option_list=option_list))


#Fetch data from biomart
ensembl = useMart("ensembl")
ensembl = useDataset("hsapiens_gene_ensembl",mart=ensembl)
biotypes = getBM(attributes = c("ensembl_gene_id", "gene_biotype"), mart = ensembl)
protein_coding_genes = biotypes[biotypes$gene_biotype == "protein_coding",]$ensembl_gene_id

#Get all transcripts
trs = getBM(attributes = c("ensembl_gene_id", "gene_biotype","ensembl_transcript_id", "transcript_biotype", "transcript_status","external_transcript_id"), 
	filters = c("ensembl_gene_id"), 
	values = protein_coding_genes, 
	mart = ensembl)

#Keep only known protein coding transcripts
trs_filtered = trs[trs$transcript_biotype == "protein_coding" & trs$transcript_status == "KNOWN" & trs$transcript_biotype == "protein_coding",]
write.table(trs_filtered, opt$t, quote = FALSE, sep = "\t", row.names = FALSE)


