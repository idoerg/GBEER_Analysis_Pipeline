#!/usr/bin/env python

import os
import sys
from Bio import SeqIO,SeqFeature
import re
CURRENT_DIR = os.path.dirname(os.path.abspath('../Utilities/Utilities.py'))
sys.path.append(os.path.dirname(CURRENT_DIR))
import Utilities.Utilities as util
import shutil

##This function filter the species with complete genome from PATRIC.
##This will also creates a new genome data folder for the family and filter out the strains
def getSpeciesListFromPATRIC(genomeFinderFilePath,bacterialGenomeDBPath,familyDBPath):
    genomeAccesionDict = {}
    genomePathDict = {}    
    genomeFinder = open(genomeFinderFilePath,"r")
    for line in genomeFinder:
        lineData = line.split("\t")
        genomeName = lineData[1].strip()
        genomeStatus = lineData[21].strip()
        accession = lineData[19].strip() 
        if(genomeStatus.strip()=="complete" and (not accession.strip()=="-") and (not accession.strip()=="")):
            genomeAccesionDict.update({accession:genomeName})
                
    genomeFinder.close()
    #out = open("/home/jain/Gram_Positive_Bacteria_Study/Organisms_Lists_from_PATRIC/Firmicutes/genomeAccessionMapfromPATRIC.txt","w")
    #out.write("Accession Number\tOrganism Name\n")
    for key,value in genomeAccesionDict.iteritems():
        genomePathDict.update({key:"null"})
        #out.write(key+"\t"+value+"\n")
    #out.close()
    genomesPath = util.return_recursive_dir_files(bacterialGenomeDBPath)
    genomePathDict = searchGenomes(genomesPath, genomeAccesionDict, genomePathDict)
    #Copy files to a new folder
    finalDir = familyDBPath
    #print genomePathDict
    for key,value in genomePathDict.iteritems():
        if value != "null":
            #print value
            name = value.split("/")[len(value.split("/"))-1]
            shutil.copytree(value, finalDir+"/"+name)
    #Filter For Strains
    distinctSpeciesGenomeLocationDict = filterStrainsByFolderName(finalDir)
    #print len(distinctSpeciesGenomeLocationDict)
    deleteDir(finalDir, distinctSpeciesGenomeLocationDict)
    filterStrain(distinctSpeciesGenomeLocationDict)
    #distinctSpeciesDict = filterStrain(distinctSpeciesGenomeLocationDict);
    #print len(distinctSpeciesDict)
    #deleteDir(finalDir, distinctSpeciesDict)
    
    
    
def searchGenomes(genomesPath,genomeAccesionDict,genomePathDict):
    for genome in genomesPath:
        genomeFiles = util.return_recursive_files(genome)
        for genomeFile in genomeFiles:
            fileName = os.path.basename(genomeFile)
            accession = ""
            for key in genomeAccesionDict.iterkeys():
                accessions = key.strip().split(",")
                #print accessions
                for a in accessions:
                    if "." in a:
                        accession = a.split(".")[0]
                    else:
                        accession = a
                    if(accession in fileName):
                        genomePathDict.update({key:genome})
                        break
    return genomePathDict

def filterStrainsByFolderName(finalDir):
    genomesDir = util.return_recursive_dir_files(finalDir)
    distinctSpeciesGenomeLocationDict = {}
    for dir in genomesDir:
        dirSplit = dir.split("/")
        strainName = "_".join(dirSplit[len(dirSplit)-1].split("_")[:2])
        #file = util.return_recursive_files(dir)[0]
        if distinctSpeciesGenomeLocationDict.has_key(strainName):
            lastOrgPath = distinctSpeciesGenomeLocationDict[strainName]
            newOrgPath = checkAccession(lastOrgPath,dir)
            distinctSpeciesGenomeLocationDict.update({strainName:newOrgPath})
        else:
            distinctSpeciesGenomeLocationDict.update({strainName:dir})
    return  distinctSpeciesGenomeLocationDict   
               
def filterStrain(distinctSpeciesGenomeLocationDict):
    distinctSpeciesDict = {}
    distinctSpeciesDict_1 = {}
    for key,value in distinctSpeciesGenomeLocationDict.iteritems():
        strainName = key;
        folderPath = value;
        #print folderPath
        #print str(return_recursive_files(folderPath)) + "\n"
        #print strainName
        for f in util.return_recursive_files(folderPath):
            seq_record = SeqIO.parse(open(f), "genbank").next()
            accession = seq_record.annotations['accessions'][0]
            organism_tmp = seq_record.annotations['organism'].replace(' ', '_')
            organism_tmp_1 = re.sub('[\[\]]', "", organism_tmp)
            organism = '_'.join(organism_tmp_1.split('_')[:2])#+"_"+accession
            #print organism
            if(distinctSpeciesDict.has_key(organism)):
                oldFilePath = distinctSpeciesDict[organism]
                old_record = SeqIO.parse(open(oldFilePath), "genbank").next()
                old_accession = old_record.annotations['accessions'][0]
                if(old_accession > accession):
                    shutil.rmtree(os.path.dirname(oldFilePath))
                    distinctSpeciesDict.update({organism:f})
                else:
                    shutil.rmtree(os.path.dirname(f))
            else:
                distinctSpeciesDict.update({organism:f})
    #for key,value in distinctSpeciesDict.iteritems():
        #distinctSpeciesDict_1.update({key:os.path.dirname(value)})
    #return distinctSpeciesDict_1
            
def checkAccession(lastOrgPath,newPath):
    lastOrgFile = util.return_recursive_files(lastOrgPath)[0]
    newOrgFile = util.return_recursive_files(newPath)[0]
    oldAccession = int(os.path.splitext(os.path.basename(lastOrgFile))[0].split("_")[1])
    newAccession = int(os.path.splitext(os.path.basename(newOrgFile))[0].split("_")[1])
    if oldAccession > newAccession:
        return newPath
    else:
        return lastOrgPath
    
def deleteDir(finalDir,distinctSpeciesGenomeLocationDict):
    dir = util.return_recursive_dir_files(finalDir)
    for d in dir:
        dirSplit = d.split("/")
        strainName = "_".join(dirSplit[len(dirSplit)-1].split("_")[:2])
        if distinctSpeciesGenomeLocationDict.has_key(strainName):
            if distinctSpeciesGenomeLocationDict[strainName] != d:
                shutil.rmtree(d)
        else:
            #shutil.rmtree(d)
            print "not matching "+strainName 
        

def main():
    genomeFinderFilePath = sys.argv[1]
    bacterialGenomeDBPath = sys.argv[2]
    familyDBPath = sys.argv[3]
    getSpeciesListFromPATRIC(genomeFinderFilePath,bacterialGenomeDBPath,familyDBPath)

if __name__ == "__main__":
    main()
            