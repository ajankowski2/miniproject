# miniproject
Human cytomegalovirus (HCMV) analysis pipeline

# Summary: 
A python wrapper was developed to execute mulitple software tools to complete the analysis of Human cytomegalovirus, abbreviated HCMV. Two patient donors were compared two and six days post infection. Methods used include converting transcriptomes to paired-end fastq files, using kallisto, sleuth, Bowtie2, SPAdes, as well as Python for a few calculations and putting together the whole pipeline.

# What to have installed:
Unix: kallisto, Bowtie2, SPAdes, Blast+

Rstudio: sleuth package, dplyr package

Python: Biopython-import Entrez and SeqIO; import os to run unix commands

# How to use the code:
1. Download all of the files to your directory
2. In the directory 'miniproject', run the python_wrapper.py file with the test data provided
3. All of the outputs can be found in the miniProject.log file and my project directory miniProject_Anne_Jankowski
