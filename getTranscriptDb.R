#Download complete transcript DB from biomart
suppressPackageStartupMessages(library(optparse))
library("biomaRt")
library("GenomicFeatures")

option_list <- list(
make_option(c("-t", "--txdb"), type="character", default=NULL,
help="Path to txdb file.", metavar = "path")
)
opt <- parse_args(OptionParser(option_list=option_list))

txdb = makeTranscriptDbFromBiomart(biomart = "ensembl",dataset = "hsapiens_gene_ensembl")
saveDb(txdb, opt$t)