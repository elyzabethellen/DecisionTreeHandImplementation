#Danny Byrd and Elizabeth E. Esterly
#pythontree.py
#last revision 09/26/2017
import cProfile, pstats, StringIO
import pdb
import matplotlib.pyplot as plt
from data import *
import csv
import math 
import random 
import copy
import collections


def getClassGAIN(data,attribute,attributeValue,classToPredict,summaryData):
	
	resultSet = {}
	runningSum = 0
	attributeValues = summaryData[classToPredict]
	dataSize = len([row[attribute] for row in data if row[attribute] == attributeValue])
	for value in attributeValues[:-1]:
		itemLengths = len([row[attribute] for row in data if row[attribute] == attributeValue and row[classToPredict] == value])
		if itemLengths > 0:
			resultSet[value] = itemLengths
		runningSum = runningSum + itemLengths

	finalAttribute = dataSize - runningSum
	if finalAttribute > 0:
		resultSet[attributeValues[-1]] = finalAttribute

	return resultSet


########getGain()########
# data :      the dataset
# attribute : attribute /column name
# returns a dictionary with attribute values = keys and counts = values.

def getKeys(data,attribute):
	return list(set([row[attribute] for row in data]))

def getGAIN(data,attribute,summaryData):
	
	#slowest verison of this loop... (at 14 seconds )

	resultSet = {}
	keys = summaryData[attribute]
	size = len(data)
	runningSum = 0
	for v in keys[:-1]:
		attributeLength = len([row[attribute] for row in data if row[attribute] == v]) 
		if attributeLength > 0:
			resultSet[v] = len([row[attribute] for row in data if row[attribute] == v]) 
			runningSum = runningSum + resultSet[v]
		# if k == len(keys) - 1:
		# 	break 

	#print(keys[:-1],keys[-1])
	#resultSet[keys[-1]] = (size - runningSum)
	finalAttribute = (size - runningSum)
	if finalAttribute > 0:
		resultSet[keys[-1]] = finalAttribute
	
	return resultSet
	
	'''
	#slowest verison of this loop... (at 16 seconds )
	resultSet = {}
	for row in data:
		if row[attribute] not in resultSet.keys():
			resultSet[row[attribute]] = 1
		else:
			resultSet[row[attribute]]+= 1
	return resultSet
	'''
	
  	
#####entropy() ######
# calculates the entropy for a given set of values 
# values :: a list of values  
def entropy(values):
	result = 0.0
	totalSize = float(sum(values)) 
	for value in values:
		result = result - (value/totalSize) * math.log((value/totalSize),2)
	return result


##### informationGain #############
# calculates the information gain for splitting on an attribute
# value
# predict0n
# data

def informationGain(value,predictOn,data,summaryData):
	baseGain = getGAIN(data,value,summaryData)
	totalGain = getGAIN(data,predictOn,summaryData)
	ig = entropy(totalGain.values()) 
	for key in baseGain.keys():		
		gainSum = getClassGAIN(data,value,key,predictOn,summaryData)
		prob = float(sum(gainSum.values()))/float(sum(totalGain.values())) 
		ig = ig - prob * entropy(getClassGAIN(data,value,key,predictOn,summaryData).values())
	return ig

##### splitData #############
# organize data by a key

def splitData(data,attribute,summaryData):
	# d = {} 
	# for key in getValues(summaryData,attribute):
	# 	d[key] = [row[attribute] for row in data if row[attribute] == key]
	# return d 
	'''
	import collections

	result = collections.defaultdict(list)

	for d in dict_list:
    	result[d['event']].append(d)

	result_list = result.values()
	'''
	'''
	result = collections.defaultdict(list)
	for d in data:
		result[d[attribute]].append(d)
	return result
	'''
	
	
	d = {} 
	for key in getValues(summaryData,attribute):
		d[key] = []
	for item in data:
		d[item[attribute]].append(item)
	return d
	


##### getValues ###### 
# gets all possible values for a particular attribute 
# data :: a data set 
# attribute :: attribute whose values to check

def getValues(summaryData,attribute):
	return summaryData[attribute]

##### getGainValues ###### 
# created a list of attributes for a dataset, sorted by best gain to worst 
def getGainValues(data,attributes,target,summaryData):
	ig = []
	keys = []
	whitelist = ["id","DNA","Class"]
	for key in attributes:
		if key not in whitelist:
			keys.append(key)
			ig.append(informationGain(key,target,data,summaryData)) # create X new subsets based on the highest split ... recursively do this, this splits are of size 1

	newAttribute = list(map((lambda x: x[1]), sorted(zip(ig, keys), reverse=True)))  #sorted(zip(ig, keys), reverse=True) #sorted(zip(ig, keys), reverse=True)
	return newAttribute

##### getGiniValues ###### 
# created a list of attributes for a dataset, sorted by best gini to worst 
def getGiniValues(data,attributes,target,summaryData):
	ig = []
	keys = []
	whitelist = ["id","DNA","Class"]
	for key in attributes:
		if key not in whitelist:
			keys.append(key)
			ig.append(giniIndex(data,key,target,summaryData)) # create X new subsets based on the highest split ... recursively do this, this splits are of size 1

	newAttribute = list(map((lambda x: x[1]), sorted(zip(ig, keys), reverse=False)))  #sorted(zip(ig, keys), reverse=True) #sorted(zip(ig, keys), reverse=True)
	return newAttribute


def getBestGain(data,attributes,target,summaryData):
	ig = []
	keys = []
	for key in attributes:
		keys.append(key)
		ig.append(informationGain(key,target,data,summaryData)) # create X new subsets based on the highest split ... recursively do this, this splits are of size 1
	newAttribute = sorted(zip(ig, keys), reverse=True)
	return newAttribute[0]

####### chiTester ##########
#for testing a single attribute
#
def chiTester(confidence, data, attribute, TA, summaryData):

	if confidence == 0:
		return True
	
	attAndCounts = getGAIN(data, attribute, summaryData)
	classAndCounts = getGAIN(data, TA, summaryData)
	df = (len(attAndCounts) - 1) * (len(classAndCounts) - 1)  # degrees of freedom
	if df == 0:
		return False

	#sort by class first
	rowSums = 0.0
	for i in range(0, len(classAndCounts)):

		#and then tally by feature value
		for a in range(0, len(attAndCounts)):
			attAndClassCount = 0

			for r in data:
				if r.get(attribute) == attAndCounts.keys()[a] and r.get(TA) == classAndCounts.keys()[i]:
					attAndClassCount += 1

		expected = attAndCounts.values()[a] * (float(classAndCounts.values()[i]) / len(data))
		
		#print("RS ADD VAL",(attAndClassCount - expected ),(attAndClassCount - expected), expected)
		rowSums += (attAndClassCount - expected ) * (attAndClassCount - expected) / expected
	#index corresponds to df
	fiftyPercentConf = [0.0, 0.004, 0.103, 0.352, 0.711, 1.145, 1.635, 2.167, 2.733, 3.325, 3.940]
	ninetyFivePercentConf = [0.0, 3.841, 5.991, 7.815, 9.488, 11.070, 12.592, 14.067, 15.507, 16.919, 18.307, 19.675]
	ninetyNinePercentConf = [0.0, 6.635, 9.210, 11.34, 13.28, 15.09, 16.81, 18.48, 20.09, 21.67, 23.21]
	twentyFivePercentConf = [0.0, 5.024, 7.378, 9.348, 11.143, 12.833, 14.449, 16.013, 17.535, 19.023, 20.483]


	if confidence == 0.25:
		if twentyFivePercentConf[df] < rowSums:
			return True
	if confidence == 0.5:
		if fiftyPercentConf[df] < rowSums:
			return True
	if confidence == 0.95:
		if ninetyFivePercentConf[df] < rowSums:
			return True
	if confidence == 0.99:
		if ninetyNinePercentConf[df] < rowSums:
			return True



	return False


#######chiSquared ##########
# for testing multiple attributes
# stub as it may be useful in the future
# using chiTester instead
def chiSquared(data, attributes, TA, summaryData):
	for i in range(0, len(attributes)):
		theChi = chiTester(data, attributes[i], TA, summaryData)
		print theChi
	return

####### giniIndex ###########
#data:       dataset
#attribute : attribute/feature column
#returns the GINI for a single column split
#to giniIndex for comparison against other column scores
def giniIndex(data, attribute, TA, summaryData):
	giniGain = 0.0
	x = getGAIN(data, attribute, summaryData)
	classifications = getValues(summaryData, TA)

	for attributeValue in x:
		acc = 0.0
		classBasedCounts = getClassGAIN(data,attribute,attributeValue,TA,summaryData)
		denominator = sum(classBasedCounts.values())
		for item in classBasedCounts.values():
			acc = acc + float(item)/denominator * float(item)/denominator
		giniGain += float(denominator)/len(data) * (1 - acc)		
	return giniGain
	

#######getBestGiniGain()#########
#data: the dataset to process
#lower GiniGain val is better with 0 being ideal
#returns a list (Gini value, Attribute)

def getBestGiniGain(attributes, data, TA, summaryData):
	bestGiniScore = float('inf')
	bestAttribute = None

	#list comprehension gives us feature columns only
	
	for singleAttribute in attributes:

		attributeScore = giniIndex(data, singleAttribute, TA, summaryData)
		#print(attributeScore,bestGiniScore)
		if attributeScore < bestGiniScore:
			bestGiniScore = attributeScore
			bestAttribute = singleAttribute
		
	return [bestGiniScore, bestAttribute]


###### mostCommonValue ######
# gets the most common value for an attribute in a dataset
# dataset :: data set 
# attribute :: attribute to search
def mostCommonValue(dataset,attribute,summaryData):
	dataResult = splitData(dataset,attribute,summaryData)
	maxKey = ""
	maxLength = 0
	for key in dataResult.keys():
		if len(dataResult[key]) > maxLength:
			maxKey = key 
			maxLength = len(dataResult[key]) 
	return maxKey

###### bID3 ######
#  this is the ID3 algorithm, runs by making a node, and then creating children 
#  if there is a decision to split 
#
#  data :: a data set
#  TA :: the target attribute to predict 
#  attributes :: set of attributes to test (this list shrinks as the algo runs)
#  whitelist :: attributes the algorithm will ignore (id , class ...etc )
def bID3(depth,examples,TA,attributes,whitelist,summaryData,MAX_DEPTH=None,TREE_DEPTH=[],chiValue=None,selection="GAIN"):
	# examples ... training examples
	# target attribute... value to be predicted
	# attributes to be tested 

	depth = depth + 1	

	TREE_DEPTH.append(depth)

	for i in whitelist:
		if i in attributes:
			attributes.remove(i)

	treeRoot = TNode()
	#treeRoot.setValue(mostCommonValue(examples,TA))
	#all examples are the same...so roll with it

	mostCommonTarget = mostCommonValue(examples,TA,summaryData)
	treeRoot.setCommonValue(mostCommonTarget)


	if len(getValues(summaryData,TA)) == 1:		
		treeRoot.setLabel(mostCommonTarget)
		return treeRoot

	if len(attributes) == 0:
		treeRoot.setLabel(mostCommonTarget)
		return treeRoot

	if selection == "GAIN":
		gainAttribute = getBestGain(examples,attributes,TA,summaryData)[1]
	else:
		gainAttribute = getBestGiniGain(attributes, examples, TA, summaryData)[1]

	if not (chiTester(chiValue, examples, gainAttribute, TA, summaryData)):	
		treeRoot.setLabel(mostCommonTarget)
		return treeRoot

	if chiValue == 0:
		if MAX_DEPTH == depth:
			treeRoot.setLabel(mostCommonTarget)
			return treeRoot

	attributes.remove(gainAttribute)
	branchValues = getValues(summaryData,gainAttribute)
	dataSplit = splitData(examples,gainAttribute,summaryData)

	for key in dataSplit.keys():
		if len(dataSplit[key]) == 0:
			treeRoot.setDecisionAttribute(gainAttribute)
			newNode = TNode()
			newNode.setLabel(mostCommonValue(examples,TA,summaryData))
			treeRoot.addChild(key,newNode)
		else:
			treeRoot.setDecisionAttribute(gainAttribute)
			treeRoot.setDecisionAttribute(gainAttribute)			
			newNode = bID3(depth,dataSplit[key],TA,copy.copy(attributes),whitelist,summaryData,MAX_DEPTH,TREE_DEPTH,chiValue,selection)
			treeRoot.addChild(key,newNode)			

	
	return treeRoot







###### crossValidate ######
#  runs a cross validation test system...splits data passed in into train and test and reports an accuracy on test 
#  runs a cross validation test system...splits data passed in into train and test and reports an accuracy on test 
#  rounds :: the number of rounds to run the model for 
#  data :: a data set
#  predictionClass :: the attribute in the data set which is getting predicted  


def crossValidate(whitelist,summaryData,rounds,data,predictionClass,maxDepth,chiValue,gainTest = "GAIN"):
	results = []

	for i in range(0,rounds):
		dataSplit = createValidationTestSet(data)
		depthCollection = []

		tree = bID3(0,dataSplit['train'],predictionClass,dataSplit['train'][0].keys(),whitelist,summaryData,maxDepth,depthCollection,chiValue,gainTest) #train the model
		for item in dataSplit['test']:
			item["guess"] = tree.classify(item)

		#print("MAX DEPTH=",max(depthCollection))

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




###### TNode ######
#  this is a node of the created decision tree 
#  children :: lookup table, which gives us the ability to traverse nodes in the tree 
#  attribute :: if the node is a decision node, attribute is the decision attribute 
#  hasAttribute :: this checks if the node is a decision node 
#  setLabel :: if node is a leaf, label is the actual value, (not attribute) used
#  classify :: classifies a given data row, into a target class (note this isn't a recursive functio)
#  addChild :: attaches a child node to this node

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
		
		'''
		each node's children set is actually a dictionary, with each key being the split decision attribute, 
		and the result from the lookup table is the next node... to get to the bottom we just use the 
		value to be classified (dataRow[currentNode.attribute]) to lookup the right child 
		'''

		currentNode = self
		while currentNode.hasAttribute():			
			if dataRow[currentNode.attribute] not in currentNode.children.keys():
				return currentNode.commonValue
			else:
				currentNode = currentNode.children[dataRow[currentNode.attribute]] 			
		
		return currentNode.label

	
	def addChild(self,key,child):
		self.children[key] = child
