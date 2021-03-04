import os
#calculate how many reads in each transcriptome before and after the Bowtie2 mapping
#first append count for before to one file
os.system('wc -1 < SRR5660030.1_1.fastq >> before')
os.system('wc -l < SRR5660033.1_1.fastq >> before')
os.system('wc -l < SRR5660044.1_1.fastq >> before')
os.system('wc -l < SRR5660045.1_1.fastq >> before')

#then append count for after mapping to a separate file
os.system('wc -l < SRR5660030.1_mapped.1.fq >> after')
os.system('wc -l < SRR5660033.1_mapped.1.fq >> after')
os.system('wc -l < SRR5660044.1_mapped.1.fq >> after')
os.system('wc -l < SRR5660045.1_mapped.1.fq >> after')
#each read has 4 lines, so we have to divide by 4 to get the right count
#this is getting the count for before

b = open('before').read().strip().split('\n')
get_lengthb = list(map(int, b))
get_lengthb = [l/4 for l in get_lengthb]

#count for after
a = open('after').read().strip().split('\n')
get_lengtha = list(map(int, b))
get_lengtha = [l/4 for l in get_lengtha]

#write how many reads in each transcriptome before and after the Bowtie2 mapping
output = open('miniProject.log', 'a')
output.write('Donor 1 (2dpi) had ' + str(get_lengthb[0]) + ' read pairs before Bowtie2 filtering and '+ str(get_lengtha[0]) +' read pairs after.')
output.write('Donor 1 (6dpi) had ' + str(get_lengthb[1]) + ' read pairs before Bowtie2 filtering and '+ str(get_lengtha[1]) +' read pairs after.')
output.write('Donor 3 (2dpi) had ' + str(get_lengthb[2]) + ' read pairs before Bowtie2 filtering and '+ str(get_lengtha[2]) +' read pairs after.')
output.write('Donor 3 (6dpi) had ' + str(get_lengthb[3]) + ' read pairs before Bowtie2 filtering and '+ str(get_lengtha[3]) +' read pairs after.')
output.close()
