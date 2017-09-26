#Danny Byrd and Elizabeth Esterly
#pythontree.py
#last revision 09/26/2017
import cProfile, pstats, StringIO


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

##### entropy ###### 
# calculates the entropy for a given set of values 
# values :: a list of values  
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


##### getValues ###### 
# gets all possible values for a particular attribute 
# data :: a data set 
# attribute :: attribute whose values to check
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


#######giniIndex()###########
#data:       dataset
#attribute : attribute/feature column
#returns the GINI for a single column split
#to giniIndex for comparison against other column scores
def giniIndex(data, attribute):
	#getGain gives us attribute counts
	x = getGAIN(data, attribute)
	print x
	#do the calculations
	return 0

#######getBestGiniGain()#########
#data: the dataset to process
#lower GiniGain val is better with 0 being ideal
#returns a list (Gini value, Attribute)
def getBestGiniGain(data):
	baseScore = float('inf')
	k = rowData[0].keys()
	blacklist = ['Class', 'id', 'DNA']
	#list comprehension gives us feature columns only
	k = [x for x in k if x not in blacklist]
	for i in range(0, len(k)):
		attributeScore = giniIndex(data, k[i])
	return


###### mostCommonValue ######
# gets the most common value for an attribute in a dataset
# dataset :: data set 
# attribute :: attribute to search
def mostCommonValue(dataset,attribute):
	dataResult = splitData(dataset,attribute)
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

	#print(len(getValues(examples,TA)))

	if len(getValues(examples,TA)) == 1:
		treeRoot.setLabel(mostCommonTarget)
		#print("beans")
		return treeRoot

	if len(attributes) == 0:
		treeRoot.setLabel(mostCommonTarget)
		return treeRoot
	# [1] is the column name in the list...[0] is the score
	#giniAttribute = getBestGiniGain(attributes)[1]
	#attributes.remove(gainAttribute)
	gainAttribute = getBestGain(examples,attributes,TA)[1]
	attributes.remove(gainAttribute)

	branchValues = getValues(examples,gainAttribute)
	dataSplit = splitData(copy.deepcopy(examples),gainAttribute)

	for key in dataSplit.keys():
		if len(dataSplit[key]) == 0:
			treeRoot.setDecisionAttribute(gainAttribute)
			# treeRoot.setDecisionAttribute(giniAttribute)
			newNode = TNode()
			newNode.setLabel(mostCommonValue(examples,TA))
			treeRoot.addChild(key,newNode)
		else:
			treeRoot.setDecisionAttribute(gainAttribute)
			#treeRoot.setDecisionAttribute(giniAttribute)
			newNode = bID3(dataSplit[key],TA,copy.copy(attributes),whitelist)
			treeRoot.addChild(key,newNode)			

	
	return treeRoot

###### createValidationTestSet ######
#  takes a data set an splits it (in half), outputs a dictionary with key for train and test with data divided between those
#  data :: a data set to split 
def createValidationTestSet(data):
	dataset = copy.deepcopy(data) 
	random.shuffle(dataset)	
	train_data = copy.deepcopy(dataset[:len(dataset)/2])
	test_data = copy.deepcopy(dataset[len(dataset)/2:])
	return {
		"train":train_data,
		"test":test_data
	}

###### crossValidate ######
#  runs a cross validation test system...splits data passed in into train and test and reports an accuracy on test 
#  rounds :: the number of rounds to run the model for 
#  data :: a data set
#  predictionClass :: the attribute in the data set which is getting predicted  
def crossValidate(rounds,data,predictionClass):
	results = []
	for i in range(0,rounds):
		dataSplit = createValidationTestSet(data)
		#for key in dataSplit:
		#	print(key,dataSplit[key])	
		#print(len(dataSplit['train']))
		tree = bID3(dataSplit['train'],predictionClass,dataSplit['train'][0].keys(),["id","Class","DNA"]) #train the model
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

count = 0
rowData = []
attribute = "Class"
with open('weatherTraining.csv') as csvfile:
	reader = csv.DictReader(csvfile)	
	for row in reader:
		rowData.append(row)

'''
# FIRST PIECE OF THE PROFILER... 
pr = cProfile.Profile()
pr.enable()
'''
print("VALIDATION SCORE",crossValidate(10,rowData,"Class")) 

'''
# THIS IS THE SECOND PIECE OF THE PROFILER, UNCOMMENT THIS TO SEE PROFILER IN ACTION
pr.disable()
s = StringIO.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print s.getvalue()
# END OF THE PROFILER!
''' 

#datas = createValidationTestSet(rowData)


tree = bID3(rowData,attribute,rowData[0].keys(),["id",attribute]) #train the model
#print(tree.attribute)
#print(tree.classify(rowData[1]))
#print(tree.children)
#for k in tree.children.keys():
#	print(k,tree.children[k].children)


# tree = bID3(rowData,attribute,rowData[0].keys(),["id",attribute]) #train the model
# print(tree.attribute)
# print(tree.classify(rowData[1]))
# print(tree.classify(rowData[2]))
# print(tree.classify(rowData[3]))
# print(tree.classify(rowData[4]))
# print(tree.classify(rowData[5]))
# print(tree.children)
# for k in tree.children.keys():
# 	print(k,tree.children[k].children)
# 	for i in tree.children[k].children.keys():
# 		print("I",i.label)

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



#########
#testing Gini stuff here
getBestGiniGain(rowData)