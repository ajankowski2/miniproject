import os
from Bio import Entrez
from Bio import SeqIO

#make the output files requested
os.system("mkdir miniProject_Anne_Jankowski")
os.system("touch miniProject.log")
#path = '/homes/ajankowski2'
os.chdir("miniProject_Anne_Jankowski")

#PART1
#use wget to download the file for each transcriptome
#donor1/2. 2/6 days post infection
d1_2 = 'https://sra-downloadb.be-md.ncbi.nlm.nih.gov/sos2/sra-pub-run-11/SRR5660030/SRR5660030.1'
d1_6 = 'https://sra-downloadb.be-md.ncbi.nlm.nih.gov/sos2/sra-pub-run-11/SRR5660033/SRR5660033.1'
d3_2 = 'https://sra-downloadb.be-md.ncbi.nlm.nih.gov/sos2/sra-pub-run-11/SRR5660044/SRR5660044.1'
d3_6 = 'https://sra-downloadb.be-md.ncbi.nlm.nih.gov/sos2/sra-pub-run-11/SRR5660045/SRR5660045.1'

os.system("wget" + d1_2)
os.system("wget" + d1_6)
os.system("wget" + d3_2)
os.system("wget" + d3_6)

#next convert each to a paried-end fastq file
os.system("fastq-dump -I --split-files SRR5660030.1")
os.system("fastq-dump -I --split-files SRR5660033.1")
os.system("fastq-dump -I --split-files SRR5660044.1")
os.system("fastq-dump -I --split-files SRR5660045.1")

#PART 2
#use kallisto to quantify TPM in each sample; first build transcriptome index for HCMV (EF999921)
os.system('python3 GenBank_CDS.py')

#PART 3
#use R package sleuth to find differentially expressed genes between the two timepoints 2 and 6
#FDR < 0.05
#include a header row, tab delimit each row
#rows = target_id test_stat pval qval

#first create index of the transcriptome reference that kallisto will use for quantification using HCMVsequence.txt
os.system('mkdir index')
os.system('time kallisto index -i index/index.idx HCMVsequence.txt')

#make a directory for the kallisto outputs
os.system("mkdir HCMV_out")
os.chdir("HCMV_out")
#directory for each output to access in R table
os.system("mkdir SRR5660030.1")
os.system("mkdir SRR5660033.1")
os.system("mkdir SRR5660044.1")
os.system("mkdir SRR5660045.1")

#once the index is built, quanitfy each sample, send to correct output location
os.system('time kallisto quant -i index/index.idx -o HCMV_out/SRR5660030.1 -b 30 -t2 SRR5660030.1_1.fastq SRR5660030.1_2.fastq')
os.system('time kallisto quant -i index/index.idx -o HCMV_out/SRR5660033.1 -b 30 -t2 SRR5660033.1_1.fastq SRR5660033.1_2.fastq')
os.system('time kallisto quant -i index/index.idx -o HCMV_out/SRR5660044.1 -b 30 -t2 SRR5660044.1_1.fastq SRR5660044.1_2.fastq')
os.system('time kallisto quant -i index/index.idx -o HCMV_out/SRR5660045.1 -b 30 -t2 SRR5660045.1_1.fastq SRR5660045.1_2.fastq')

##use the R package sleuth to find differentially expressed genes between the two timepoints (2pi and 6dpi) 
os.system('Rscript proj_sleuth.R')
os.system("cd miniProject_Anne_Jankowski")
os.system('cat R_results.txt >> miniProject.log')
###PART 4
#use bowtie 2 to create an index for HCMV (EF999921)
#command file index name 
os.system('bowtie2-build HCMVsequence.txt hcmv')
#save the reads that map to this transcriptome index
os.system('bowtie2 --quiet -x hcmv -1 SRR5660030.1_1.fastq -2 SRR5660030.1_2.fastq -S hcmvmap.sam --al-conc SRR5660030.1_mapped.fq')
os.system('bowtie2 --quiet -x hcmv -1 SRR5660033.1_1.fastq -2 SRR5660033.1_2.fastq -S hcmvmap.sam --al-conc SRR5660033.1_mapped.fq')
os.system('bowtie2 --quiet -x hcmv -1 SRR5660044.1_1.fastq -2 SRR5660044.1_2.fastq -S hcmvmap.sam --al-conc SRR5660044.1_mapped.fq')
os.system('bowtie2 --quiet -x hcmv -1 SRR5660045.1_1.fastq -2 SRR5660045.1_2.fastq -S hcmvmap.sam --al-conc SRR5660045.1_mapped.fq')

#calculate how many reads in each transcriptome before and after the Bowtie2 mapping
#get counts, append to beforeb and afterb file and then use py script
#first append count for before to one file
os.system('wc -l < SRR5660030.1_1.fastq >> beforeb')
os.system('wc -l < SRR5660033.1_1.fastq >> beforeb')
os.system('wc -l < SRR5660044.1_1.fastq >> beforeb')
os.system('wc -l < SRR5660045.1_1.fastq >> beforeb')

#then append count for after mapping to a separate file
os.system('wc -l < SRR5660030.1_mapped.1.fq >> afterb')
os.system('wc -l < SRR5660033.1_mapped.1.fq >> afterb')
os.system('wc -l < SRR5660044.1_mapped.1.fq >> afterb')
os.system('wc -l < SRR5660045.1_mapped.1.fq >> afterb')

#run the python script to get the lengths and print to log file
os.system('python3 Bowtie2_lens.py')

#use SPAdes to produce 1 assembly of all four transcriptomes
#write SPAdes command to log file
os.system('spades -k 55,77,99,127 -t 2 --only-assembler --pe1-1 SRR5660030.1_mapped.1.fq --pe1-2 SRR5660030.1_mapped.2.fq --pe2-1 SRR5660033.1_mapped.1.fq --pe2-2 SRR5660033.1_mapped.2.fq --pe3-1 SRR5660044.1_mapped.1.fq  --pe3-2 SRR5660044.1_mapped.2.fq --pe4-1 SRR5660045.1_mapped.1.fq --pe4-2 SRR5660045.1_mapped.2.fq -o project_assembly/')
#append output of this command to the minproject log file
os.system('echo "spades -k 55,77,99,127 -t 2 --only-assembler --pe1-1 SRR5660030.1_mapped.1.fq--pe1-2 SRR5660030.1_mapped.2.fq --pe2-1 SRR5660033.1_mapped.1.fq --pe2-2 SRR5660033.1_mapped.2.fq --pe3-1 SRR5660044.1_mapped.1.fq  --pe3-2 SRR5660044.1_mapped.2.fq --pe4-1 SRR5660045.1_mapped.1.fq --pe4-2 SRR5660045.1_mapped.2.fq -o project_assembly/" >> miniProject.log')

##PART 6
#write python script to calculate the number of contigs with length > 1000
os.system('python3 ContigLength.py')

#PART 7
#write python script to calculate the length of the assembly
os.system('python3 AssemblyLength.py')

#PART 8
#write python script to retrieve longest contig from SPAdes assembly
#os.system('python3 ()')
#make local database 
          
