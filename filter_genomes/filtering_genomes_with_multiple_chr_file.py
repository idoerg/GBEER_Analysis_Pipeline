#!/usr/bin/env python

import os,sys
from Bio import SeqIO
CURRENT_DIR = os.path.dirname(os.path.abspath('../Utilities/Utilities.py'))
sys.path.append(os.path.dirname(CURRENT_DIR))
import Utilities.Utilities as util
import shutil

def filterGenomes(rootDir):
    filter_genomes_list = {}
    for file in util.return_recursive_dir_files(rootDir):
        #print file
        files = util.return_recursive_files(file)
        fileName = ""
        if len(files) > 1:
            for f in files:
                seq_record = SeqIO.parse(open(f), "genbank").next()
                accession = seq_record.annotations['accessions'][0]
                definition = seq_record.description;
                if ("plasmid" not in definition):
                    if fileName != "":
                        #print os.path.dirname(os.path.abspath(f))
                        filter_genomes_list.update({os.path.dirname(os.path.abspath(f)):""})
                    fileName = accession+".gbk"
            for f in files:
                if os.path.basename(f) != fileName:
                    #print f
                    os.remove(f)
    ##Deleting all the genomes having multiple chromosomes files
    #print len(filter_genomes_list)
    for folder in filter_genomes_list.iterkeys():
        shutil.rmtree(folder)
    
        
def main():
    rootDir = sys.argv[1];
    #print rootDir
    #rootDir = "/home/jain/test_genomes_folder"
    filterGenomes(rootDir)

if __name__ == "__main__":
    # CURRENT_DIR = os.path.dirname(os.path.abspath('../Utilities/Utilities.py'))
    # sys.path.append(os.path.dirname(CURRENT_DIR))
    main()
