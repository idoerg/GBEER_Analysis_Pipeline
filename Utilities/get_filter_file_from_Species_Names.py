#!/usr/bin/env python

import Utilities as util
import sys
from Bio import SeqIO
import re

def printAccessionNumbersFromName(filePath,dbFolderPath,outFolder):
    file = open(filePath,"r")
    o = open(outFolder+"/filter.txt","w")
    org = []
    accessions = []
    for line in file:
        temp = '_'.join(line.split("_")[:2])
        org.append(temp.strip())
    for dir in util.return_recursive_dir_files(dbFolderPath):
        dirSplit = dir.split("/")
        organism = ""
        accession = ""
        for f in util.return_recursive_files(dir):
            #print f
            seq_record = SeqIO.parse(open(f), "genbank").next()
            accession = seq_record.annotations['accessions'][0]
            organism_tmp = seq_record.annotations['organism'].replace(' ', '_')
            organism_tmp_1 = re.sub('[\[\]]', "", organism_tmp)
            organism = '_'.join(organism_tmp_1.split('_')[:2])#+"_"+accession
        try:
            if(org.index(organism) >= 0):
                accessions.append(accession)
        except:
            #print "none"
            pass
    for accesion in accessions:
        o.write(accesion+"\n")            
    o.close()
    file.close()
    
def main():
    filePath = sys.argv[1]
    dbPath = sys.argv[2]
    outFolder = sys.argv[3]
    printAccessionNumbersFromName(filePath,dbPath,outFolder)
        
if __name__ == "__main__":
    main()