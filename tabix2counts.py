rm $1/fc.pex.gz
for J in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 X Y
#for J in 1 
do 
        tabix $1/$1.tbx.gz $J | ~/bin/countReadChrom ~/Ensembl/PatchExon/chr$J.gz -exon | gzip >> $1/fc.pex.gz
done