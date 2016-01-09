import sys
import os
import argparse
import fileinput
import subprocess

parser = argparse.ArgumentParser(description = "Convert RASQUAL output into a SQLite database that can be accessed with dplyr in R.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--indir", help = "Directory of the input files.")
parser.add_argument("--insuffix", help = "Suffix of the input file.", default = ".txt")
parser.add_argument("--outdir", help = "Directory of the output files.")
parser.add_argument("--prefix", help = "Prefix of the input RASQUAL file and output SQLite files.")
parser.add_argument("--sqlite3_bin", help = "Path to the SQLite3 executable.", default = "sqlite3")
args = parser.parse_args()

#Construct SQL file for SQlite
sql_path = os.path.join(args.outdir, args.prefix + ".sql")
rasqual_path = os.path.join(args.indir, args.prefix + args.insuffix)
sql_file = open(sql_path, "w")
create_table = "create table rasqual(gene_id text, snp_id text, chr text, pos int, allele_freq real, chisq real, effect_size real, n_feature_snps int, n_cis_snps int, converged int);\n"
sql_file.write(create_table)
sql_file.write('.separator "\\t"' + "\n")
sql_file.write(".import " + rasqual_path + " rasqual\n")

#Create indexes
sql_file.write("CREATE INDEX idx1 ON rasqual(gene_id);\n")
sql_file.write("CREATE INDEX idx2 ON rasqual(snp_id);\n")
sql_file.write("CREATE INDEX idx3 ON rasqual(chr, pos);\n")
sql_file.write(".exit\n")
sql_file.close()

#run sqlite
db_path = os.path.join(args.outdir, args.prefix + ".sqlite3")
command = " ".join(["cat", sql_path, "|", args.sqlite3_bin, db_path])
subprocess.call(['bash','-c',command])