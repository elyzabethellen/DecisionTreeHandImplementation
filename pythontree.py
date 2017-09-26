#Danny Byrd and Elizabeth Esterly
#pythontree.py
#last revision 09/25/2017

import csv
import math 
import random 
import copy

def getClassGAIN(data,attribute,attributeValue,classToPredict):
	resultSet = {}
	for row in data:
		if row[attribute] == attributeValue:
			if row[classToPredict] not in resultSet:
				resultSet[row[classToPredict]] = 1
			else:
				resultSet[row[classToPredict]] = resultSet[row[classToPredict]] + 1

	return resultSet


########getGain()########
# data :      the dataset
# attribute : attribute /column name
# returns a dictionary with attribute values = keys and counts = values.
def getGAIN(data,attribute):
	resultSet = {}
	for row in data:
		if row[attribute] not in resultSet.keys():
			resultSet[row[attribute]] = 1
		else:
			resultSet[row[attribute]]+= 1
	return resultSet

def entropy(values):
	result = 0.0
	totalSize = float(sum(values)) 
	for value in values:
		result = result - (value/totalSize) * math.log((value/totalSize),2)
	return result

def informationGain(value,predictOn,data):
	baseGain = getGAIN(rowData,value)
	totalGain = getGAIN(rowData,predictOn)
	ig = entropy(totalGain.values()) 
	for key in baseGain.keys():		
		gainSum = getClassGAIN(data,value,key,predictOn)
		prob = float(sum(gainSum.values()))/float(sum(totalGain.values())) 
		ig = ig - prob * entropy(getClassGAIN(data,value,key,predictOn).values())

	return ig


def splitData(data,attribute):
	d = {} 
	for key in getValues(data,attribute):
		d[key] = []
	
	for item in data:
		d[item[attribute]].append(item)

	return d

def getValues(data,attribute):
	dictionary = {}
	for row in data:
		dictionary[row[attribute]] = 1

	return dictionary.keys()

def getBestGain(data,attributes,target):
	ig = []
	keys = []
	for key in attributes:
		keys.append(key)
		ig.append(informationGain(key,target,data)) # create X new subsets based on the highest split ... recursively do this, this splits are of size 1
			#print(key,informationGain(key,"Class",rowData))

	#print(sorted(zip(ig, keys), reverse=True))
	newAttribute = sorted(zip(ig, keys), reverse=True)
	return newAttribute[0]

def giniIndex(data):
	k = rowData[0].keys()

	for i in range(0, len(k)):
		if k[i] != 'id' and k[i] != 'Class':
			x = getGAIN(rowData, k[i])
			print x
	return 0

def getBestGini():
	#lower GINI is better
	return 0


def mostCommonValue(dataset,attribute):
	dataResult = splitData(dataset,attribute)
	maxKey = ""
	maxLength = 0
	for key in dataResult.keys():
		if len(dataResult[key]) > maxLength:
			maxKey = key 
			maxLength = len(dataResult[key]) 
	return maxKey

def bID3(examples,TA,attributes,whitelist):
	# examples ... training examples
	# target attribute... value to be predicted
	# attributes to be tested 
	for i in whitelist:
		if i in attributes:
			attributes.remove(i)
	
	treeRoot = TNode()
	#treeRoot.setValue(mostCommonValue(examples,TA))
	#all examples are the same...so roll with it 

	mostCommonTarget = mostCommonValue(examples,TA)
	treeRoot.setCommonValue(mostCommonTarget)

	if getValues(examples,TA) == 1:		
		treeRoot.setLabel(mostCommonTarget)
		return treeRoot

	if len(attributes) == 0:
		treeRoot.setLabel(mostCommonTarget)
		return treeRoot

###########INSERT ARG TO DECIDE GINI OR INFO GAIN HERE
	######################################################################
	gainAttribute = getBestGain(examples,attributes,TA)[1]
	attributes.remove(gainAttribute)

	branchValues = getValues(examples,gainAttribute)
	dataSplit = splitData(copy.deepcopy(examples),gainAttribute)

	for key in dataSplit.keys():
		if len(dataSplit[key]) == 0:
			treeRoot.setDecisionAttribute(gainAttribute)
			newNode = TNode()
			newNode.setLabel(mostCommonValue(examples,TA))
			treeRoot.addChild(key,newNode)
		else:
			treeRoot.setDecisionAttribute(gainAttribute)			
			newNode = bID3(dataSplit[key],TA,copy.copy(attributes),whitelist)
			treeRoot.addChild(key,newNode)			

	# if all the examples are positive... 
	# if there are no more attributes... 
	
	return treeRoot

def createValidationTestSet(data):
	dataset = copy.deepcopy(data) 
	random.shuffle(dataset)	
	train_data = copy.deepcopy(dataset[:len(dataset)/2])
	test_data = copy.deepcopy(dataset[len(dataset)/2:])
	return {
		"train":train_data,
		"test":test_data
	}

def crossValidate(rounds,data,predictionClass):
	results = []
	for i in range(0,rounds):
		dataSplit = createValidationTestSet(data)
		#for key in dataSplit:
		#	print(key,dataSplit[key])	

		print(len(dataSplit['train']))
		tree = bID3(dataSplit['train'],predictionClass,dataSplit['train'][0].keys(),["id","Class"]) #train the model
		for item in dataSplit['test']:
			item["guess"] = tree.classify(item)

		wrong = 0
		correct = 0
		total = len(dataSplit['test'])
		for item in dataSplit['test']:
			if item['guess'] == item[predictionClass]:
				correct+=1 
			else:
				wrong+=1 
		setResult = float(correct)/float(total)
		results.append(setResult)
		dataSplit = {}
	return sum(results) / float(len(results)) 

class TNode:
	attribute = ""
	label = ""
	children = {}
	commonValue = ""

	def __init__(self):
		self.children = {}
		self.attribute = None
		self.commonValue = ""

	def hasAttribute(self):
		if self.attribute == None:
			return False
		else:
			return True

	def setCommonValue(self,cm):
		self.commonValue = cm 

	def setLabel(self,label):
		self.label = label 

	def setDecisionAttribute(self,attribute):
		self.attribute = attribute
	
	def classify(self,dataRow):
	
		currentNode = self
		while currentNode.hasAttribute():
			#print(currentNode.children,dataRow[currentNode.attribute],currentNode.attribute)
			if dataRow[currentNode.attribute] not in currentNode.children.keys():
				return currentNode.commonValue
			else:
				currentNode = currentNode.children[dataRow[currentNode.attribute]] 			
		
		return currentNode.label

	
	def addChild(self,key,child):
		self.children[key] = child

count = 0
rowData = []
attribute = "Class"
with open('weatherTraining.csv') as csvfile:
	reader = csv.DictReader(csvfile)	
	for row in reader:
		rowData.append(row)

#print("VALIDATION SCORE",crossValidate(1,rowData,"Class")) 
#datas = createValidationTestSet(rowData)

tree = bID3(rowData,attribute,rowData[0].keys(),["id",attribute]) #train the model
#print(tree.attribute)
#print(tree.classify(rowData[1]))
#print(tree.children)
#for k in tree.children.keys():
#	print(k,tree.children[k].children)




# this is kinda a debugger haha
# datas = createValidationTestSet(rowData)
# tree = bID3(datas['train'],"Class",rowData[0].keys(),["id","Class"]) #train the model
# for i in datas['train']:
# 	print(i)
# print(" ==== ==== ==== ==== ===== ")
# for k in datas['test']:
# 	print(k)
# print(" ==== ==== ==== ==== ===== ")
#print("Classification",tree.classify(datas['test'][1]))



