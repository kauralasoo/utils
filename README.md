# utils
This repository contains a loose collection of scripts that that use to work with sequencing data. Most of them are probably only useful for myself, but I've made them public, because there is no reason to keep them private. Majority of the scripts are wrappers around commonly used tools. Below is a short description of some the scripts that might be more broadly useful.

## rasqual
Scripts designed to simplify running [RASQUAL](https://github.com/dg13/rasqual) on a large number of samples. 
* `bamCountASE.py` - Uses ASEReadCounter from the Genome Analysis Toolkit (GATK) to quantify allele-specifc expression in RNA-Seq BAM files.
* `mergeASECounts.py` - Merges alle-specifc read counts from the previous script into a single table.
* `vcfAddASE.py` - Adds allele-specifc counts from `mergeASECounts.py` into a VCF file.
* `runRasqual.py` - Run RASQUAL on a batch of genes.

