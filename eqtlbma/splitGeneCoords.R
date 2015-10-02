suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(optparse))

option_list <- list(
  make_option(c("-i", "--input"), type="character", default=NULL,
              help="Path to the input BED file.", metavar = "path"),
  make_option(c("-o", "--output"), type="character", default=NULL,
              help="Path to the file mapping batch ids to gene ids.", metavar = "path"),
  make_option(c("-b", "--batch_size"), type="character", default = "NULL", 
              help = "Number of genes in each batch", metavar = "INT")
)
opt <- parse_args(OptionParser(option_list=option_list))

splitIntoBatches <- function(n, batch_size){
  # Given a total number of elements n and batch size, contruct a vector of length n where
  # each element occurs at most batch_size times.
  n_batches = ceiling(n/batch_size)
  batch_ids = rep(seq(1:n_batches), each = batch_size)[1:n]
  return(batch_ids)
}

#Import BED file of gene coordinates
gene_coords = read.table(opt$i, stringsAsFactors = FALSE)
colnames(gene_coords) = c("chr","start","end","gene_id", "score","strand")
gene_coords = dplyr::arrange(gene_coords, chr, start)
batch_size = as.numeric(opt$b)

#Count the number of genes per chromosome
gene_count = dplyr::group_by(gene_coords, chr) %>% summarize(gene_count = length(gene_id))
gene_batches = dplyr::left_join(gene_coords, gene_count, by = "chr") %>%
  dplyr::group_by(chr) %>% 
  dplyr::mutate(batch_number = splitIntoBatches(gene_count[1], batch_size)) %>%
  dplyr::mutate(batch_id = paste("chr", chr, "batch", batch_number, sep = "_")) %>%
  dplyr::group_by(batch_id) %>%
  dplyr::summarize(gene_ids = paste(gene_id, collapse = ";"))

#Save the batch assignments onto disk
write.table(gene_batches, opt$o, sep = "\t", row.names = FALSE, col.names = FALSE, quote = FALSE)

