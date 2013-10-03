suppressPackageStartupMessages(library(optparse))

option_list <- list(
make_option(c("-s", "--samples"), type="character", default=NULL,
	help="Path to sample id-name mapping.", metavar = "path"),
make_option(c("-c", "--counts"), type="character", default=NULL,
	help="Path to counts folder.", metavar = "path"),
make_option(c("-o", "--out"), type="character", default = "NULL", 
	help = "Path to output file", metavar = "path")
)
opt <- parse_args(OptionParser(option_list=option_list))

#Read sample names and ids
table = read.table(opt$s, comment.char = "")
ids = as.vector(table[,1])
names = as.vector(table[,2])

loadCounts <- function(count_folder, ids, names){
	matrix = c()
	for (i in c(1:length(ids))){
		path = file.path(count_folder, paste(ids[i], ".txt", sep = ""))
		table = read.table(path, header = TRUE)
		if (i == 1){
			matrix = table
		}
		else{
			matrix = cbind(matrix, table[,3])
		}
	}
	colnames(matrix) = c("geneid", "length", names)
	return(matrix)
}

count_table = loadCounts(opt$c, ids, names)
rownames(count_table) = count_table$geneid
print(head(count_table))
write.table(count_table, opt$o, quote = FALSE, sep = "\t")