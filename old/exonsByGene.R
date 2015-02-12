# Extract exons from txtb object, merge exons by gene and export into BED file

#Parse command line options
suppressPackageStartupMessages(library(optparse))

option_list <- list(
make_option(c("-t", "--transcript-db"), type="character", default=NULL,
help="Path to TranscriptDb object.", metavar = "path"),
make_option(c("-b", "--bed"), type="character", default=NULL,
help="Path to BED file.", metavar = "path")
)
opt <- parse_args(OptionParser(option_list=option_list))

if (is.null(opt$t) | is.null(opt$b)){
	write("Need to specify TranscriptDb and output BED file. See --help for usage.", stderr())
	quit("no",1)
}

#Load TranscriptDb from disk
suppressPackageStartupMessages(library(rtracklayer))
suppressPackageStartupMessages(library(GenomicFeatures))
txdb = loadDb(opt$t)

#Keep only primary chromosomes
isActiveSeq(txdb)[seqlevels(txdb)] = FALSE
isActiveSeq(txdb)[seqlevels(txdb)[1:25]] = TRUE

#Extract exons for all genes
exonsByGene = exonsBy(txdb, by="gene")
exonsByGene = reduce(exonsByGene)

#Save results to disk
export(exonsByGene, opt$b, format = "BED")