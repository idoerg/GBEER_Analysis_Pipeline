#!/usr/bin/env python

import numpy as np
import os
import Utilities as util
import sys

def creating_filter_list(infolder):
    files = util.return_recursive_files(infolder)
    filterFile = open("filter.txt","w")
    for file in files:
        accession = file.split("/")[6].split(".")[0]
        filterFile.write(accession)
        filterFile.write("\n")
    filterFile.close()
    
def main():
    rootDir = sys.argv[0];
    creating_filter_list(rootDir)
        
if __name__ == "__main__":
    main()