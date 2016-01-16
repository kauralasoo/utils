suppressPackageStartupMessages(library("GenomicRanges"))
suppressPackageStartupMessages(library("plyr"))
suppressPackageStartupMessages(library("dplyr"))
suppressPackageStartupMessages(library("optparse"))

#Parse command line options
option_list <- list(
  make_option(c("-s", "--snp-coords"), type="character", default=NULL,
              help="Path to the text file with SNP coordinates (chr, pos, id).", metavar = "path"),
  make_option(c("-e", "--exon-coords"), type="character", default=NULL,
              help="Path to the text file with exon start/end coordinates (gene_id, chromosome_name, strand, exon_starts, exon_ends).", metavar = "path"),
  make_option(c("-c", "--counts"), type="character", default=NULL,
              help="Path to the the output file with SNP counts per gene.", metavar = "path"),
  make_option(c("-w", "--window"), type="integer", default=500000,
              help="Size of the cis window in bp.",
              metavar="number")
)
opt <- parse_args(OptionParser(option_list=option_list))

if (is.null(opt$s) | is.null(opt$e)| is.null(opt$c)){
  write("Need to specify the SNP and exon coordinates text files as well as output counts file. See --help for usage.", stderr())
  quit("no",1)
}

#Import SNP coordinates from a text file
snp_coords = read.table(opt$s, stringsAsFactors = FALSE)
snp_granges = GRanges(seqnames = snp_coords[,1], ranges = IRanges(start = snp_coords[,2], end = snp_coords[,2]))

#Import exon coordinates
union_exon_coords = read.table(opt$e, stringsAsFactors = FALSE, header = TRUE)
union_exon_coords = dplyr::mutate(union_exon_coords, exon_starts = as.character(exon_starts), exon_ends = as.character(exon_ends))

#Create a df of exon coords
exon_df = ldply(dlply(union_exon_coords, .(gene_id), 
    function(x){
        data.frame(gene_id = x$gene_id, 
                        chromosome_name = x$chromosome_name,
                        strand = x$strand,
                        exon_start = as.numeric(unlist(strsplit(x$exon_starts,","))),
                        exon_end = as.numeric(unlist(strsplit(x$exon_ends,",")))
        )
      }
    )
  )
exon_df$gene_id = as.character(exon_df$gene_id)
exon_granges = GRanges(seqnames = exon_df$chromosome_name, ranges = 
                         IRanges(start = exon_df$exon_start, end = exon_df$exon_end), strand = exon_df$strand)
mcols(exon_granges) = data.frame(gene_id = exon_df$gene_id, stringsAsFactors = FALSE)

#Count the number of feature SNPS per gene
olaps = findOverlaps(exon_granges, snp_granges) %>% as.data.frame()
olaps = dplyr::mutate(olaps, gene_id = exon_granges$gene_id[olaps$queryHits])
feature_snp_count = dplyr::group_by(olaps, gene_id) %>% dplyr::summarise(feature_snp_count = length(subjectHits)) %>%
  dplyr::mutate(gene_id = as.character(gene_id))

#Count the number of cis SNPs per gene
gene_window = dplyr::group_by(exon_df, gene_id) %>% summarise(start = min(exon_start), end = max(exon_end))

#Define windows around the TSS
TSS_window = dplyr::group_by(exon_df, gene_id) %>% 
  summarise(chromosome_name = chromosome_name[1], start = ifelse(max(strand) == 1, min(exon_start), max(exon_end)))
TSS_granges = GRanges(seqnames = TSS_window$chromosome_name, 
                      IRanges(start = pmax(TSS_window$start - opt$w, 0), end = TSS_window$start + opt$w))
mcols(TSS_granges) = data.frame(gene_id = TSS_window$gene_id)

TSS_olaps = findOverlaps(TSS_granges, snp_granges) %>% as.data.frame()
TSS_olaps = dplyr::mutate(TSS_olaps, gene_id = as.character(TSS_granges$gene_id)[TSS_olaps$queryHits])
TSS_cis_snps_count = dplyr::group_by(TSS_olaps, gene_id) %>% dplyr::summarise(cis_snp_count = length(subjectHits))

#Combine both feature SNP and cis SNP counts into one data.frame
TSS_df = as.data.frame(TSS_granges) %>% tbl_df() %>% 
  dplyr::transmute(gene_id = as.character(gene_id), chr = seqnames, range_start = start, range_end = end) %>% 
  dplyr::left_join(feature_snp_count, by = "gene_id") %>% 
  dplyr::left_join(TSS_cis_snps_count, by = "gene_id")
TSS_df[is.na(TSS_df)] = 0

#Add SNP counts into the original data.frame and write results to disks
snp_counts = dplyr::select(TSS_df, gene_id, range_start, range_end, feature_snp_count, cis_snp_count)
result = dplyr::left_join(union_exon_coords, snp_counts, by = "gene_id")
write.table(result, opt$c, row.names = FALSE, sep ="\t", quote = FALSE)

