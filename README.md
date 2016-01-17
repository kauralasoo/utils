# utils
This repository contains a loose collection of scripts that that use to work with sequencing data. Most of them are probably only useful for myself, but I've made them public, because there is no reason to keep them private. Majority of the scripts are wrappers around commonly used tools. Below is a short description of some the scripts that might be more broadly useful.

## rasqual
Scripts designed to simplify running [RASQUAL](https://github.com/dg13/rasqual) on a large number of samples. 
* `bamCountASE.py` - Uses ASEReadCounter from the Genome Analysis Toolkit (GATK) to quantify allele-specifc expression in RNA-Seq BAM files.
* `mergeASECounts.py` - Merges allele-specifc read counts from the previous script into a single table.
* `vcfAddASE.py` - Adds allele-specifc counts from `mergeASECounts.py` into a VCF file.
* `runRasqual.py` - Run RASQUAL on a batch of genes.

## bam
Scripts for processing BAM files.
* `bamToFragmentBed.py` - Use bedtools to convert paired-end BAM file into a BED file of fragments.

## vcf
Scripts for processing VCF files.
* `liftoverVcfGenotypes.py` - Uses [CrossMap.py](http://crossmap.sourceforge.net/) to lift over VCF file from hg19 coordinates to GRCh38 coordinates.
