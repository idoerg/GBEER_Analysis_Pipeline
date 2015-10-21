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
from atk import Util

def getSpeciesListFromPATRIC():
    genomeAccesionDict = {}
    genomePathDict = {}    
    genomeFinder = open("/home/jain/Gram_Positive_Bacteria_Study/Organisms_Lists_from_PATRIC/Firmicutes/GenomeFinder.txt","r")
    for line in genomeFinder:
        lineData = line.split("\t")
        genomeName = lineData[1].strip()
        genomeStatus = lineData[21].strip()
        accession = lineData[19].strip() 
        if(genomeStatus.trim().equals("complete") and (not accession.trim().equals("-")) and (not accession.trim().equals(""))):
            genomeAccesionDict.update({accession, genomeName})
                
    genomeFinder.close()
    out = open("/home/jain/Gram_Positive_Bacteria_Study/Organisms_Lists_from_PATRIC/Firmicutes/genomeAccessionMapfromPATRIC.txt","w")
    out.write("Accession Number\tOrganism Name\n")
    for key,value in genomeAccesionDict.iteritems():
        genomePathDict.update({key,"null"})
        out.write(key+"\t"+value+"\n")
    out.close()
    genomesPath = util.return_recursive_dir_files("/home/jain/Bacterial_Genomic_Data_NCBI/")
    genomePathDict = searchGenomes(genomesPath, genomeAccesionDict, genomePathDict)
    #Copy files to a new folder
    finalDir = ""
    for key,value in genomePathDict.iteritems():
        if value != "null":
            shutil.copytree(value, finalDir)
    #Filter For Strains
    
def searchGenomes(genomesPath,genomeAccesionDict,genomePathDict):
    for genome in genomesPath:
        genomeFiles = util.return_recursive_files(genome)
        for genomeFile in genomeFiles:
            fileName = os.path.basename(genomeFile)
            accession = ""
            for key in genomeAccesionDict.iterkeys():
                accessions = key.strip().split(",")
                for a in accessions:
                    if "." in a:
                        accession = a.split(".")[0]
                    else:
                        accession = a
                if(accession in fileName):
                    genomePathDict.update({accessions,genome})
                break
    return genomePathDict

def filterStrainsByFolderName(finalDir):
    genomesDir = util.return_recursive_dir_files(finalDir)
    distinctSpeciesGenomeLocationDict = {}
    for dir in genomesDir:
        strainName = "_".join(dir.split("_")[:2])
        #file = util.return_recursive_files(dir)[0]
        if distinctSpeciesGenomeLocationDict.has_key(strainName):
            lastOrgPath = distinctSpeciesGenomeLocationDict[strainName]
            newOrgPath = checkAccession(lastOrgPath,dir)
            distinctSpeciesGenomeLocationDict.update({strainName,newOrgPath})
        else:
            distinctSpeciesGenomeLocationDict.update({strainName,dir})    
               
            
def checkAccession(lastOrgPath,newPath):
    lastOrgFile = util.return_recursive_files(lastOrgPath)[0]
    newOrgFile = util.return_recursive_files(newPath)[0]
    oldAccession = int(os.path.splitext(os.path.basename(lastOrgFile))[0].split("_")[1])
    newAccession = int(os.path.splitext(os.path.basename(newOrgFile))[0].split("_")[1])
    if oldAccession > newAccession:
        return newPath
    else:
        return lastOrgPath
    
    
    
    
    
    
    
            
            