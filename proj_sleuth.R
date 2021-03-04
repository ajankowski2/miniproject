library(sleuth)
stab <- read.table('sleuth_table.txt', header=TRUE,stringsAsFactors =FALSE)
so <- sleuth_prep(stab)
#fit a model comparing the two conditions 
so <-sleuth_fit(so, ~condition,'full')
#fit the reduced model to compare in the likelihood ratio test 
so <- sleuth_fit(so, ~1, 'reduced')
#perform the likelihood ratio test for differential expression between conditions
so <- sleuth_lrt(so, 'reduced', 'full')


library(dplyr)
#extract the test results from the sleuth object
sleuth_table <- sleuth_results(so, 'reduced:full', 'lrt', show_all = FALSE) 
#filter most significant results and sort by pval
sleuth_significant <- dplyr::filter(sleuth_table, qval <= 0.05)

#just show the target id, test stat, pval, and qval
project <-dplyr::select(sleuth_significant, target_id, test_stat, pval, qval)
#show first ten of what I need to check
head(project, n=10)

#write project data to file
write.table(project, file="fdr05_results.txt",quote = FALSE,row.names = TRUE)
