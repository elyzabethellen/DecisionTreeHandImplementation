# basic data analysis
import csv, random
from featureBuilder import preprocessData

CROSS_VALIDATION_FACTOR = 10 # this is the number of parts in a split of test to train, 
# so if you set this to say 4 ... your training data will consit of 3/4 of data, and test will be 1/4
 

###### parseDataFile ######
#  takes an input file and outputs an array of dictionaries with the data 
#  csvName :: a csvName set to load 
def parseDataFile(csvName,startingKeys = ["id","DNA","Class"]):
	rowData = []
	with open(csvName) as csvfile:
		reader = csv.DictReader(csvfile,startingKeys)	
		keys = {}
		for row in reader:
			keys = row.keys()
			rowData.append(row)
	return rowData

###### writeDataFile ######
def writeDataFile(outCSV,dataset,keys):
	with open(outCSV, "wb") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		writer.writerow(keys)		
		for line in dataset:
			listData = []
			for k in keys:			
				if k in line:
					listData.append(line[k])				
			writer.writerow(listData)


###### createValidationTestSet ######
#  takes a data set an splits it (in half), outputs a dictionary with key for train and test with data divided between those
#  data :: a data set to split 
def createValidationTestSet(data):
	
	dataset = data
	random.shuffle(dataset)	

	factor = CROSS_VALIDATION_FACTOR

	train_data = dataset[:(factor - 1)*len(dataset)/factor]
	for row in train_data:
		if "guess" in row:
			del row["guess"]

	test_data = dataset[(factor - 1)*len(dataset)/factor:]

	return {
		"train":train_data,
		"test":test_data
	}


###### createOutSubmission ######
#  takes a source CSV, and fills the CSV with predictions based on tree passed in 
#  sourceCSV :: source CSV to input
#  outputCSV :: output CSV to use 
def createOutSubmission(sourceCSV,outputCSV,tree):
	
	newKaggleData = preprocessData(parseDataFile(sourceCSV,["id","DNA"]))

	for row in newKaggleData:
		row["class"] = tree.classify(row)

	writeDataFile(outputCSV,newKaggleData,["id","class"])

###### buildSummaryData ######
#  takes input data set and gives table of each attribute/value in the data (so this doesn't need to happen on the fly)
#  dataset :: data
def buildSummaryData(dataset):
	summaryTable = {}
	keys = dataset[0].keys()
	for key in keys:
		summaryTable[key] = list(set([row[key] for row in dataset]))
		#print(key,list(set([row[key] for row in dataset])))

	return summaryTable


