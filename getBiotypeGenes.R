#Get biotype information for each gene from biomart
suppressPackageStartupMessages(library(optparse))
library("biomaRt")

option_list <- list(
make_option(c("-b", "--biotypes"), type="character", default=NULL,
help="Path to gene biotypes text file.", metavar = "path")
)
opt <- parse_args(OptionParser(option_list=option_list))

ensembl = useMart("ensembl")
ensembl = useDataset("hsapiens_gene_ensembl",mart=ensembl)
biotypes = getBM(attributes = c("ensembl_gene_id", "gene_biotype"), mart = ensembl)
write.table(biotypes, opt$b, quote = FALSE, row.names = FALSE)
