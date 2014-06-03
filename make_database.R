## make sqlite database from all.txt

library(devtools)
install_github('read.csv.sql', 'alyssafrazee')
library(read.csv.sql) 

dbfile = 'dat.db'
cat(file=dbfile)
statement = paste0('create table main.github as select * from file')
read.csv.sql('allh.txt', sql=statement, dbname=dbfile, sep='\t')



