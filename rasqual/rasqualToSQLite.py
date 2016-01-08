--Create table
create table rasqual(gene_id text, snp_id text, chr text, pos int, allele_freq real, chisq real, effect_size real, n_feature_snps int, n_cis_snps int, converged int);

--Import data
.separator "\t"
.import naive.tsv rasqual 

--Create indeces
CREATE INDEX idx1 ON rasqual(gene_id);
CREATE INDEX idx2 ON rasqual(snp_id);
CREATE INDEX idx3 ON rasqual(chr, pos);
