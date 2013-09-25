loadCounts <- function(count_folder, ids){
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
	colnames(matrix) = c("geneid", "length", ids)
	return(matrix)
}

ids = c("10506_0#1","10506_0#2","10506_0#3","10506_0#4","10506_0#5","10506_0#6","10506_0#7","10506_0#8")
count_table = loadCounts("counts/", ids)
rownames(count_table) = count_table$geneid
write.table(count_table, "counts/count_table.txt")