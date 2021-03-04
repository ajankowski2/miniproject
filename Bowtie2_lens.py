#each read has 4 lines, so we have to divide by 4 to get the right count
#this is getting the count for before mapping
b = open('beforeb').read().rstrip()
get_lengthb = b.split('\n')
#get counts in list, map allows iteration of get_lengthb
get_lengthb = list(map(int, get_lengthb))
#divide by 4 to get right count
get_lengthb = [l//4 for l in get_lengthb]

#count for after
a = open('afterb').read().rstrip()
get_lengtha = a.split('\n')
#get counts in list, map allows iteration of get_lengtha
get_lengtha = list(map(int, get_lengtha))
#divide by 4 to get right count
get_lengtha = [l//4 for l in get_lengtha]

#write how many reads in each transcriptome before and after the Bowtie2 mapping
#access values in b and a lists
#open the log file and append to it
output = open('miniProject.log', 'a')
output.write('Donor 1 (2dpi) had ' + str(get_lengthb[0]) + ' read pairs before Bowtie2 filtering and '+ str(get_lengtha[0]) +' read pairs after.')
output.write('Donor 1 (6dpi) had ' + str(get_lengthb[1]) + ' read pairs before Bowtie2 filtering and '+ str(get_lengtha[1]) +' read pairs after.')
output.write('Donor 3 (2dpi) had ' + str(get_lengthb[2]) + ' read pairs before Bowtie2 filtering and '+ str(get_lengtha[2]) +' read pairs after.')
output.write('Donor 3 (6dpi) had ' + str(get_lengthb[3]) + ' read pairs before Bowtie2 filtering and '+ str(get_lengtha[3]) +' read pairs after.')
#close the log file
output.close()
