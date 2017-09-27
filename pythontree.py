#Danny Byrd and Elizabeth E. Esterly
#pythontree.py
#last revision 09/26/2017
import cProfile, pstats, StringIO
import pdb
import matplotlib.pyplot as plt

import csv
import math 
import random 
import copy


''' 
mini GA 
'''

def runTA(population):
	for thing in population:
		fitness = testFitness(thing)

def testFitness(thing):
	return 34


def mutate(Dlist,features):
	coin = random.choice([0,1])
	if coin == 1:
		featuresToAdd = set(features) - set(Dlist)
		if len(featuresToAdd) > 0:
			Dlist.append(random.choice(featuresToAdd))
	else:
		randomRemove = random.choice(Dlist)
		Dlist = Dlist.remove(randomRemove)
	return Dlist
	


	# add 
	# remove 
	



def getClassGAIN(data,attribute,attributeValue,classToPredict,summaryData):
	'''

	resultSet = {}
	for row in data:
		if row[attribute] == attributeValue:
			if row[classToPredict] not in resultSet:
				resultSet[row[classToPredict]] = 1
			else:
				resultSet[row[classToPredict]] = resultSet[row[classToPredict]] + 1

	#print(resultSet) 
	'''

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


	#1.831 without mods ... 15 with 
	#1.7?


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

def getGainValues(data,attributes,target,summaryData):
	ig = []
	keys = []
	whitelist = ["id","DNA","Class"]
	for key in attributes:
		if key not in whitelist:
			keys.append(key)
			ig.append(informationGain(key,target,data,summaryData)) # create X new subsets based on the highest split ... recursively do this, this splits are of size 1
			#print(key,informationGain(key,"Class",rowData))

	#print(sorted(zip(ig, keys), reverse=True))
	newAttribute = list(map((lambda x: x[1]), sorted(zip(ig, keys), reverse=True)))  #sorted(zip(ig, keys), reverse=True) #sorted(zip(ig, keys), reverse=True)
	return newAttribute


def getBestGain(data,attributes,target,summaryData):
	ig = []
	keys = []
	for key in attributes:
		keys.append(key)
		ig.append(informationGain(key,target,data,summaryData)) # create X new subsets based on the highest split ... recursively do this, this splits are of size 1
			#print(key,informationGain(key,"Class",rowData))

	#print(sorted(zip(ig, keys), reverse=True))
	newAttribute = sorted(zip(ig, keys), reverse=True)
	return newAttribute[0]

####### chiTester ##########
#for testing a single attribute
#
def chiTester(confidence, data, attribute, TA):
	if confidence == 0:
		return True
	attAndCounts = getGAIN(data, attribute)
	classAndCounts = getGAIN(data, TA)
	df = (len(attAndCounts) - 1) * (len(classAndCounts) - 1)  # degrees of freedom
	#sort by class first
	rowSums = 0.0
	for i in range(0, len(classAndCounts)):
		#and then tally by feature value
		for a in range(0, len(attAndCounts)):
			attAndClassCount = 0
			for r in rowData:
				if r.get(attribute) == attAndCounts.keys()[a] and r.get(TA) == classAndCounts.keys()[i]:
					attAndClassCount += 1

		expected = attAndCounts.values()[a] * (float(classAndCounts.values()[i]) / totalRows)
		rowSums += (attAndClassCount - expected ) * (attAndClassCount - expected) / expected
	#index corresponds to df
	fiftyPercentConf = [0.0, 0.004, 0.103, 0.352, 0.711, 1.145, 1.635, 2.167, 2.733, 3.325, 3.940]
	ninetyFivePercentConf = [0.0, 3.841, 5.991, 7.815, 9.488, 11.070, 12.592, 14.067, 15.507, 16.919, 18.307, 19.675]
	ninetyNinePercentConf = [0.0, 6.635, 9.210, 11.34, 13.28, 15.09, 16.81, 18.48, 20.09, 21.67, 23.21]
	if confidence == 0.5:
		if fiftyPercentConf[df] > rowSums:
			return True
	if confidence == 0.95:
		if ninetyFivePercentConf[df] > rowSums:
			return True
	if confidence == 0.99:
		if ninetyNinePercentConf[df] > rowSums:
			return True

	return False


#######chiSquared ##########
# for testing multiple attributes
# stub as it may be useful in the future
# using chiTester instead
def chiSquared(data, attributes, TA):
	for i in range(0, len(attributes)):
		theChi = chiTester(data, attributes[i], TA)
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
		giniGain += float(denominator)/totalRows * (1 - acc)		
	return giniGain



	

#######getBestGiniGain()#########
#data: the dataset to process
#lower GiniGain val is better with 0 being ideal
#returns a list (Gini value, Attribute)

def getBestGiniGain(attributes, data, TA, summaryData):
	bestGiniScore = float('inf')
	bestAttribute = None
	for i in range(0, len(attributes)):
		attributeScore = giniIndex(data, attributes[i], TA)

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
def bID3(depth,examples,TA,attributes,whitelist,summaryData,MAX_DEPTH=None):
	# examples ... training examples
	# target attribute... value to be predicted
	# attributes to be tested 

	depth = depth + 1	

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
	'''''
	#GINI INDEX
	#giniAttribute = getBestGiniGain(attributes, rowData, TA)[1]
	#
	#attributes.remove(giniAttribute)
	'''

	gainAttribute = getBestGain(examples,attributes,TA,summaryData)[1]

	'''''
	#Le CHI: needs access to confidence, maybe this can be a global
	#if not (chiTester(confidence, rowData, gainAttribute, TA)):
		#return
	'''''

	#gainAttribute = getBestGain(examples,attributes,TA)[1]


	if MAX_DEPTH == depth:
		treeRoot.setLabel(mostCommonTarget)
		return treeRoot

	#gainAttribute = getBestGiniGain(attributes, rowData, TA, summaryData)[1] 
	gainAttribute = getBestGain(examples,attributes,TA,summaryData)[1] 


	attributes.remove(gainAttribute)

	branchValues = getValues(summaryData,gainAttribute)
	dataSplit = splitData(examples,gainAttribute,summaryData)

	for key in dataSplit.keys():
		if len(dataSplit[key]) == 0:
			treeRoot.setDecisionAttribute(gainAttribute)
			# treeRoot.setDecisionAttribute(giniAttribute) #GINI INDEX
			newNode = TNode()
			newNode.setLabel(mostCommonValue(examples,TA,summaryData))
			treeRoot.addChild(key,newNode)
		else:
			treeRoot.setDecisionAttribute(gainAttribute)
			#treeRoot.setDecisionAttribute(giniAttribute) #GINI INDEX
			#newNode = bID3(dataSplit[key],TA,copy.copy(attributes),whitelist)

			treeRoot.setDecisionAttribute(gainAttribute)			
			newNode = bID3(depth,dataSplit[key],TA,copy.copy(attributes),whitelist,summaryData,MAX_DEPTH)
			treeRoot.addChild(key,newNode)			

	
	return treeRoot

###### createValidationTestSet ######
#  takes a data set an splits it (in half), outputs a dictionary with key for train and test with data divided between those
#  data :: a data set to split 
def createValidationTestSet(data):
	dataset = data#copy.deepcopy(data) 
	random.shuffle(dataset)	

	#lists[:3*len(lists)/4]
	#lists[3*len(lists)/4:]
	
	#train_data = dataset[:len(dataset)/2] #copy.deepcopy(dataset[:len(dataset)/2])
	
	factor = 10

	train_data = dataset[:(factor - 1)*len(dataset)/factor]
	for row in train_data:
		if "guess" in row:
			del row["guess"]

	test_data = dataset[(factor - 1)*len(dataset)/factor:]

	# for i in test_data:
	# 	print(i)

	return {
		"train":train_data,
		"test":test_data
	}


def createOutSubmission(inputCSV,whitelist,tree):
	data = []
	with open(inputCSV) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			data.append(row)

		newKeys = ['id','Class'] #data[0].keys()
		#newKeys.append("Class")

	for row in data:
		row["Class"] = tree.classify(row)

	with open('kaggletest.csv', "wb") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		writer.writerow(newKeys)
		print(newKeys)
		for line in data:
			listData = []
			for k in newKeys:			
				if k in line:
					listData.append(line[k])
			#print(listData)					
			writer.writerow(listData)

#createOutSubmission("subOne.csv",[],"tree")
#(['29', '31', '28', '30', '34', '27', '32']

###### crossValidate ######
#  runs a cross validation test system...splits data passed in into train and test and reports an accuracy on test 
#  runs a cross validation test system...splits data passed in into train and test and reports an accuracy on test 
#  rounds :: the number of rounds to run the model for 
#  data :: a data set
#  predictionClass :: the attribute in the data set which is getting predicted  
def crossValidate(whitelist,summaryData,rounds,data,predictionClass,maxDepth):
	results = []
	for i in range(0,rounds):
		dataSplit = createValidationTestSet(data)
		#for key in dataSplit:
		#	print(key,dataSplit[key])	
		#print(len(dataSplit['train']))
		tree = bID3(0,dataSplit['train'],predictionClass,dataSplit['train'][0].keys(),whitelist,summaryData,maxDepth) #train the model
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


def buildSummaryData(dataset):
	summaryTable = {}
	keys = dataset[0].keys()
	for key in keys:
		summaryTable[key] = list(set([row[key] for row in dataset]))
		#print(key,list(set([row[key] for row in dataset])))

	return summaryTable

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

###################################################################################################
#BEGIN SCRIPT
totalRows = 0
count = 0
rowData = []
attribute = "Class"
with open('plain.csv') as csvfile:
	reader = csv.DictReader(csvfile)	
	keys = {}
	for row in reader:
		keys = row.keys()
		rowData.append(row)
		totalRows += 1



# FIRST PIECE OF THE PROFILER... 
# pr = cProfile.Profile()
# pr.enable()

summaryData = buildSummaryData(rowData)
# #gainList = getGainValues(rowData,keys,"Class",summaryData)
# specialCandidates = ['29', '31', '28', '30', '34', '27', '32','AGGT','GGTA']
# whitelist = list(set(keys) - set(specialCandidates)) 
# tree = bID3(0,rowData,"Class",rowData[0].keys(),whitelist,summaryData,6)
# createOutSubmission("subOne.csv",whitelist,tree)

gainList = getGainValues(rowData,keys,"Class",summaryData)

count = 9
while count > 0:
	#specialCandidates = gainList[:count]
	specialCandidates = ['29', '31', '28', '30', '34', '27', '32','18'] #'AGGT','GGTA'
	whitelist = list(set(keys) - set(specialCandidates)) 
	print(specialCandidates,crossValidate(whitelist,summaryData,10,rowData,"Class",6)) 
	count = count - 1

#gainList = getGainValues(rowData,keys,"Class",summaryData)

# for i in range(1,100):
# 	gainList = random.sample(set(keys),11)
# 	specialCandidates = gainList[:count]
# 	whitelist = list(set(keys) - set(specialCandidates)) 
# 	print(gainList,crossValidate(whitelist,summaryData,10,rowData,"Class",6)) 

'''
for i in range(1,10,):
	count = 10
	print('MAX TREE=',i)
	while count > 0:
		specialCandidates = gainList[:count]
		whitelist = list(set(keys) - set(specialCandidates)) 
		print(specialCandidates,crossValidate(whitelist,summaryData,10,rowData,"Class",i)) 
		count = count - 1
'''





#summaryData = buildSummaryData(rowData)
#experimentPlots = []
#for i in range(1,2):
	#experimentPlots.append(crossValidate(summaryData,10,rowData,"Class",i)) 
#print(crossValidate(summaryData,1,rowData,"Class",None))

# plt.plot(range(1,50),experimentPlots)
# plt.ylabel('Validation Accuracy')
# plt.xlabel('Tree Size')
# plt.show()

'''
# THIS IS THE SECOND PIECE OF THE PROFILER, UNCOMMENT THIS TO SEE PROFILER IN ACTION
# pr.disable()
# s = StringIO.StringIO()
# sortby = 'cumulative'
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats()
# print s.getvalue()
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

#
if(chiTester(0.95, rowData, 'Outlook', 'Class')):
	print "YES! YES! YES! C'est fini..."

# pr = cProfile.Profile()
# pr.enable()

#testing Gini stuff here uncomment next 2 lines to test it manually

#print(len(summaryData.keys())/2)
#print(len(summaryData.keys()))
#print(summaryData.keys()[252])
#print(summaryData.keys()[251])
#del summaryData["id"]
#attributes = summaryData.keys()
#attributes.remove("Class")

#print("SGI=",sginiIndex(rowData,"L30","Class",summaryData)) 
#print("GI=",giniIndex(rowData,"L30","Class",summaryData)) 
#a = getBestGiniGain(attributes[:300],rowData,'Class', summaryData)
#print(a)
#for i in attributes:
	#print(sginiIndex(rowData,i,"Class",summaryData)) 
	#print(sginiIndex(rowData,i,"Class",summaryData)) 

#a = getBestGiniGain(attributes[:300],rowData,'Class', summaryData)
#for i in attributes[:300]:
#print(sginiIndex(rowData,i,"Class",summaryData)) 

#print("RESULT",a)
#print gTest

# pr.disable()
# s = StringIO.StringIO()
# sortby = 'cumulative'
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats()
# print s.getvalue()

