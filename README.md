# utils
This repository contains a loose collection of scripts that I use to work with sequencing data. Most of them are probably only useful for myself, but I've made them public, because there is no reason to keep them private. Majority of the scripts are wrappers around commonly used tools. Below is a short description of some the scripts that might be more broadly useful.

## bam
Scripts for processing BAM files.
* `bamToFragmentBed.py` - Use bedtools to convert paired-end BAM file into a BED file of fragments.

## vcf
Scripts for processing VCF files.
* `liftoverVcfGenotypes.py` - Uses [CrossMap.py](http://crossmap.sourceforge.net/) to lift over VCF file from hg19 coordinates to GRCh38 coordinates.

## gtf
Scripts for processing GTF files.
* `gtf2database.py` - Converts GTF/GFF file into a database used by [gffutils](http://daler.github.io/gffutils/)
* `filterGFF.py` - Select a subset of genes and transcripts from a GFF file.
