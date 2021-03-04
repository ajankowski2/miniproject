from Bio import Entrez
from Bio import SeqIO
#from Roslalind problems
Entrez.email = 'ajankowski2@luc.edu'
output = open('HCMVsequence.txt', 'w')
handle = Entrez.efetch(db = 'nucleotide', id = 'EF999921', rettype = 'gb', retmode = 'text')
record = SeqIO.read(handle, 'genbank')
#set intitial count to 0
CDS = 0
#loop to count the CDS 
for feature in record.features:
    if feature.type == 'CDS':
        CDS += 1
        #set the name as the id of the protein
        feature_name = str(feature.qualifiers['protein_id'])
        #set the sequence as found
        feature_seq = feature.extract(record.seq)
        #write HCMV CDS to HCMVsequence.txt file
        output.write('>' + feature_name + '\n' + str(feature_seq) + '\n')
#close the sequence  file        
output.close()
#open project log file and write in required info
output = open('miniProject.log', 'w')
output.write('The HCMV genome (EF999921) has ' + str(CDS) + ' CDS.')
#close log file
output.close()
