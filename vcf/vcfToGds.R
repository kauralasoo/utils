suppressPackageStartupMessages(library("SNPRelate"))
suppressPackageStartupMessages(library("optparse"))

option_list <- list(
  make_option(c("-v", "--vcf_file"), type="character", default=NULL,
              help="Path to VCF file.", metavar = "path"),
  make_option(c("-g", "--gds_file"), type="character", default=NULL,
              help="Path to the gds file.", metavar = "path")
)
opt <- parse_args(OptionParser(option_list=option_list))
SNPRelate::snpgdsVCF2GDS(opt$v, opt$g, method = "copy.num.of.ref")