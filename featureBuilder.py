import csv
import collections
import sys

rowData = []

def occurrences(string, sub):
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count+=1
        else:
            return count

def createTwoLetterPermutations():
    letterSample = ["A","T","C","G"]
    permutations = []
    for letter in letterSample:
        for secondletter in letterSample:           
            permutations.append(letter+secondletter)
    return permutations    

def createPermutations(): 
    letterSample = ["A","T","C","G"]
    permutations = []
    for letter in letterSample:
        for secondletter in letterSample:
            for thirdletter in letterSample:
                for fourthletter in letterSample:
                    permutations.append(letter+secondletter+thirdletter+fourthletter)
    return permutations

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

def threshold(thisInput,ceiling):
    if thisInput < ceiling:
        return "Y"

    return "N"

def markovmodel(stringData):

    dictionary = {} 
    for permutation in createTwoLetterPermutations():
        getFirstLetter = permutation[0]
        
        if stringData.count(permutation) > 0:
            dictionary[permutation] = fourWaySplit(float(occurrences(stringData,permutation))/float(stringData.count(getFirstLetter)))
        else:
            dictionary[permutation] = fourWaySplit(0) 
    
    return dictionary   

lock = 0



newKeys = {}

d = collections.OrderedDict() # using an ordered dict for cleaner ordering / logic 

if len(sys.argv) > 2: 
    inputCSV = sys.argv[1]
    outputCSV = sys.argv[2]
    startingKeys = ["id","DNA","Class"]


    with open(inputCSV) as csvfile:
        reader = csv.DictReader(csvfile,startingKeys)
        
        for row in reader:
            newRow = collections.OrderedDict()
            #if lock < 2: # this was just for testing 

            for k in row.keys():                
                if k == "Class":
                    if len(sys.argv) == 3:
                        newRow[k] = row[k]                        
                else:
                    newRow[k] = row[k]

            dna = row['DNA']
            #lock = lock + 1
            
            totalcount = len(dna)
            newRow["first"] = dna[0]
            newRow["last"] = dna[totalcount-1]
            newRow["25pA"] = threshold(float(dna.count("A"))/totalcount,0.25)
            newRow["25pT"] = threshold(float(dna.count("T"))/totalcount,0.25)
            newRow["25pG"] = threshold(float(dna.count("G"))/totalcount,0.25)
            newRow["25pC"] = threshold(float(dna.count("C"))/totalcount,0.25)
            
            dictionary = markovmodel(dna)
            keys = dictionary.keys()           
            for k in keys:
              newRow[k] = dictionary.get(k)

            for permutation in createPermutations():
                newRow[permutation] = "F"
                if dna.count(permutation) > 0:
                    newRow[permutation] = "T"


            counter = 0
            for letter in dna:               
                newRow[str(counter)] = dna[counter]
                counter = counter + 1 

            newKeys = newRow.keys(); 
            rowData.append(newRow)
               

    with open(outputCSV, "wb") as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(newKeys)
            for line in rowData:   
                listData = []
                for k in newKeys:               
                    if k in line:                    
                        listData.append(line[k])            
                writer.writerow(listData)
else:
    print("Please specify an input and output CSV file")
