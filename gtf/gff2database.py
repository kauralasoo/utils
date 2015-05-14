import sys
import gffutils

gff_file = sys.argv[1]
db_file = sys.argv[2]
gffutils.create_db(gff_file, db_file)