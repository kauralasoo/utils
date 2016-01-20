suppressPackageStartupMessages(library("SNPRelate"))
suppressPackageStartupMessages(library("optparse"))

option_list <- list(
  make_option(c("-v", "--vcf-directory"), type="character", default=NULL,
              help="Path to the directory containing VCF files.", metavar = "path"),
  make_option(c("-c", "--chr-list"), type="character", default=NULL,
              help="Path the file containing list of chromosomes.", metavar = "path")
)
opt <- parse_args(OptionParser(option_list=option_list))

chromosme_list = scan(opt$c, what = "character")
for (chr in chromosme_list){
	print(chr)
	vcf_file = file.path(opt$v, paste("chr_",chr,".vcf.gz", sep = ""))
	gds_file = file.path(opt$v, paste("chr_",chr,".gds", sep = ""))
	SNPRelate::snpgdsVCF2GDS(vcf_file, gds_file, method = "copy.num.of.ref")
}