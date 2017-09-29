import csv
import collections
import sys
import random

CUSTOM_FEATURES = False

rowData = []


# chooses a likely option for an unknown character
def fixDNACharacter(character):
    if character == "D":
        return random.choice(["A","G","T"])
    if character == "N":
        return random.choice(["C","A","G","T"])
    if character == "S":    
        return random.choice(["C","G"])
    if character == "R":
        return random.choice(["A","G"])
    
    return character    

# counts value in string
def occurrences(string, sub):
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count+=1
        else:
            return count

# creates a list of two letter permutations for all possible 4 letter combinations 
def createTwoLetterPermutations():
    letterSample = ["A","T","C","G"]
    permutations = []
    for letter in letterSample:
        for secondletter in letterSample:           
            permutations.append(letter+secondletter)
    return permutations    

# creates a four letter list of permutations for all possible 4 letter combinations 
def createPermutations(): 
    letterSample = ["A","T","C","G"]
    permutations = []
    for letter in letterSample:
        for secondletter in letterSample:
            for thirdletter in letterSample:
                for fourthletter in letterSample:
                    permutations.append(letter+secondletter+thirdletter+fourthletter)
    return permutations

# creates categories for intervals of a continuous input
def fourWaySplit(thisInput):
    if thisInput == 0:
        return "0"
    if thisInput < 0.25:
        return "1"
    if thisInput < 0.50:
        return "2"
    if thisInput < 0.75:
        return "3"
    if thisInput < 1.0:
        return "4"    

# creates 2 categories for intervals of a continuous input
def threshold(thisInput,ceiling):
    if thisInput < ceiling:
        return "Y"

    return "N"

# builds a dictionary which creates a state transition/ probability lookup table for a given string
def markovmodel(row):

    stringData = row["DNA"]
    dictionary = {} 
    for permutation in createTwoLetterPermutations():
        getFirstLetter = permutation[0]
        
        if stringData.count(permutation) > 0:
            dictionary[permutation] = fourWaySplit(float(occurrences(stringData,permutation))/float(stringData.count(getFirstLetter)))
        else:
            dictionary[permutation] = fourWaySplit(0) 
    
    
    keys = dictionary.keys()           
    for k in keys:
        row[k] = dictionary.get(k)

# splits a DNA string into a feature per DNA character 
def splitDNA(row):
    counter = 0
    for letter in row["DNA"]:        
        row[str(counter)] = fixDNACharacter(row["DNA"][counter])
        counter = counter + 1 
    

# track specific character counts in DNA string
def DNACharCounts(row):
    dna = row["DNA"]
    totalcount = len(dna)
    row["first"] = dna[0] #adds the first letter 
    row["last"] = dna[totalcount-1] # adds the last letter 
    row["25pA"] = threshold(float(dna.count("A"))/totalcount,0.25) # gives a positive boolean if string is greater than 25% A 
    row["25pT"] = threshold(float(dna.count("T"))/totalcount,0.25) # gives a positive boolean if string is greater than 25% T 
    row["25pG"] = threshold(float(dna.count("G"))/totalcount,0.25) # gives a positive boolean if string is greater than 25% G 
    row["25pC"] = threshold(float(dna.count("C"))/totalcount,0.25) # gives a positive boolean if string is greater than 25% C 

#adds a boolean value to the training 
def fourLetterPermutationBoolean(row): 
    dna = row["DNA"]
    for permutation in createPermutations():
        row[permutation] = "F"
        if dna.count(permutation) > 0:
            row[permutation] = "T"

# adds a column for each i+1 position, so each new column has 2 DNA letters (labeled with L)
def twoLetterFeature(row):
    dna = row["DNA"]
    for i in range(0,len(dna)-1,2):
        row["L"+str(i)] = dna[i] + dna[i+1] 

# adds a column for each i+2 position, so each new Q column has 3 DNA letters (labeled with Q)
def fourLetterFeature(row):
    dna = row["DNA"]
    for i in range(0,len(dna)-2,3):
        row["Q"+str(i)] = dna[i] + dna[i+1] + dna[i+2]       
        

#process imported CSV data, to add features, clean ETC 
def preprocessData(importedData):
    for row in importedData:
        splitDNA(row)
        # DNACharCounts(row) #-> uncomment these to add features
        # fourLetterPermutationBoolean(row) -> uncomment these to add features
        # twoLetterFeature(row) -> uncomment these to add features
        # markovmodel(row)

    return importedData

