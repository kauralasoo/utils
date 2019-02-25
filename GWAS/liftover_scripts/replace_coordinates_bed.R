library("dplyr")
library("optparse")

#Parse command-line options
option_list <- list(
  make_option(c("-s", "--summaries"), type="character", default=NULL,
              help="Old summary stats files.", metavar = "type"),
  make_option(c("-c", "--coords"), type="character", default=NULL,
              help="New coordinates of variants.", metavar = "type"),
  make_option(c("-o", "--out"), type="character", default=NULL,
              help="Output file.", metavar = "type")
)
opt <- parse_args(OptionParser(option_list=option_list))

#Specify paths
summary_path = opt$s
coords_path = opt$c
out_summary_path = opt$o

#Import GWAS summary stats
gwas_col_names = c("snp_id", "chr", "pos", "effect_allele", "MAF",
                   "p_nominal", "beta", "OR", "log_OR", "se", "z_score", "trait", "PMID", "used_file")
gwas_col_types = c("ccicdddddddccc")
gwas_pvals = readr::read_tsv(summary_path,
                             col_names = gwas_col_names, col_types = gwas_col_types, skip = 1) %>%
  dplyr::mutate(variant_id = paste(chr, pos, effect_allele, sep = "_")) %>%
  dplyr::select(-chr, -pos)

#Import updated coordinates
new_coords = readr::read_tsv(coords_path, col_names = c("chr", "pos", "pos2", "variant_id"), col_types = "ciic") %>%
  dplyr::select(chr, pos, variant_id)

#Add new coordinates
updated_gwas = dplyr::left_join(gwas_pvals, new_coords, by = "variant_id") %>%
  dplyr::select(gwas_col_names) %>%
  dplyr::filter(!is.na(pos)) %>%
  dplyr::arrange(chr, pos)

#Save file
outfile = gzfile(out_summary_path, "w")
write.table(updated_gwas, outfile, sep = "\t", quote = F, row.names = F)
close(outfile)
