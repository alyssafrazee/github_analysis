## make sqlite database from all.txt

install.packages('proto')
install.packages('DBI')
install.packages('chron')
install.packages('RSQLite')
install.packages('RSQLite.extfuns')
library(devtools)
install_github('read.csv.sql', 'alyssafrazee')
library(read.csv.sql) 

dbfile = 'dat.db'
cat(file=dbfile)
statement = 'create table main.github as select * from file'
read.csv.sql('allh.txt', sql=statement, dbname=dbfile, sep='\t')

## remove last names (for anonymity/public data release):
allh = read.table('allh.txt', comment.char="", header=TRUE, sep='\t', quote='')
ss = function(x, pattern, slot=1, ...){
    sapply(strsplit(x, pattern, ...), "[", slot)  
}
first_name = ss(as.character(allh$owner_name), pattern=' ', slot=1)
allh$owner_name = first_name
write.table(allh, file='allh_anon.txt', quote=FALSE, row.names=TRUE, 
    col.names=FALSE, sep='\t')
cat(file='dat_anon.db')
read.csv.sql('allh_anon.txt', sql=statement, dbname='dat_anon.db', sep='\t')



