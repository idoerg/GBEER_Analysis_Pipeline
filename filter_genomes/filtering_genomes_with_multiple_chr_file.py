#!/usr/bin/env python

import numpy as np
import os
from Bio import SeqIO,SeqFeature
from Bio.SeqRecord import SeqRecord
from Bio import Phylo
import re
import Utilities.Utilities as util
import shutil
import sys

def filterGenomes(rootDir):
    filter_genomes_list = []
    for file in util.return_recursive_dir_files(rootDir):
            files = util.return_recursive_files(file)
            fileName = ""
            if len(files) > 1:
                for f in files:
                    seq_record = SeqIO.parse(open(f), "genbank").next()
                    accession = seq_record.annotations['accessions'][0]
                    definition = seq_record.description;
                    if ("plasmid" not in definition):
                        if fileName != "":
                            filter_genomes_list.append(os.path.dirname(os.path.abspath(f)))
                        fileName = accession+".gbk"
                for f in files:
                    if os.path.basename(f) != fileName:
                        os.remove(f)
    ##Deleting all the genomes having multiple chromosomes files
    for folder in filter_genomes_list:
        shutil.rmtree(folder)
    
        
def main():
    rootDir = sys.argv[0];
    filterGenomes(rootDir)

if __name__ == "__main__":
    main()