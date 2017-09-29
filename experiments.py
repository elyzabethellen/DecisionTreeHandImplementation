# experiments to run for class...

from pythontree import *
from data import *
from experimentTools import *

#experiments with INFOGAIN 
#chiVALUES
#experiments with GINI
#chiVALUES

CVRounds = 20 #this is usually greater for testing 
supportedChiValues = [0.0,0.25,0.50,0.95,0.99]

def informationGainExperiments(data,summaryData):
	whitelist = ["id","Class","DNA"]
	for chi in supportedChiValues:
		print("score = ",crossValidate(whitelist,summaryData,CVRounds,data,"Class",None,chi),"-  TESTING information gain and CHI =",chi) 


def giniExperiments(data,summaryData):
	whitelist = ["id","Class","DNA"]
	for chi in supportedChiValues:
		print("score = ",crossValidate(whitelist,summaryData,CVRounds,data,"Class",None,chi,"GINI"),"-  TESTING gini and CHI =",chi) 


def kaggleSubmissionExperiment(data,summaryData):
	# NOTE this is not nesscesarily the final submission 
	
	# first build a tree with the entire data set : 
	whitelist = ["id","Class","DNA"]
	tree = bID3(0,data,"Class",data[0].keys(),whitelist,summaryData,6,[],0,"GAIN")

	# then pass to Outsubmission file 
	createOutSubmission("testing.csv","submissionSample.csv",tree)
	print("submissionSample.csv - has been created!")




def firstPlaceKaggleWork(data,summaryData):
	
	dataKeys = data[0].keys()
	whitelist = ["id","Class","DNA"]
	cleanKeys = list(set(dataKeys) - set(whitelist))

	gainSet = getGainValues(data,cleanKeys,"Class",summaryData)[:15]
	giniSet = getGiniValues(data,cleanKeys,"Class",summaryData)[:15]

	whiteListGain = buildWhiteList(gainSet,whitelist,dataKeys)
	whiteListGINI = buildWhiteList(giniSet,whitelist,dataKeys)
	whiteListSanity = buildWhiteList(['29', '31', '28', '30', '34', '27', '32'],whitelist,dataKeys)
	
	print(giniSet,gainSet)
	# print("score SANITY = ",crossValidate(whiteListSanity,summaryData,CVRounds,data,"Class",6,0.0,"GAIN"))
	# print("score GAIN LIST = ",crossValidate(whiteListGain,summaryData,CVRounds,data,"Class",6,0.0,"GAIN")) 
	# print("score GINI LIST = ",crossValidate(whiteListGINI,summaryData,CVRounds,data,"Class",6,0.0,"GAIN")) 



	#print(dataKeys)
	#whitelist = ["id","Class","DNA"]
	#print("score = ",crossValidate(whitelist,summaryData,CVRounds,data,"Class",6,0.0,"GAIN")) 
	#print("lets begin")
	''' 
	whitelist = ["id","Class","DNA"]
	tree = bID3(0,rowData,"Class",data[0].keys(),whitelist,summaryData,6,[],0,"GAIN")
	createOutSubmission("testing.csv",whitelist,tree)
	'''
