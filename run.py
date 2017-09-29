	
def program():

	from data import buildSummaryData
	from data import parseDataFile
	from experiments import informationGainExperiments
	from experiments import giniExperiments
	from experiments import kaggleSubmissionExperiment
	from experiments import firstPlaceKaggleWork
	from featureBuilder import preprocessData

	GAIN = False
	GINI = False
	KAGGLETEST = False
	KAGGLEBEST = True

	trainingData = preprocessData(parseDataFile('training.csv'))
	summaryData = buildSummaryData(trainingData)

	if GAIN: # runs information gain experiments
		informationGainExperiments(trainingData,summaryData)

	if GINI: # runs GINI experiments
		giniExperiments(trainingData,summaryData)

	if KAGGLETEST: # creates a kaggle submission
		kaggleSubmissionExperiment(trainingData,summaryData)

	if KAGGLEBEST: # tests/code we used to win the competition (off cause it takes a while)
		firstPlaceKaggleWork(trainingData,summaryData)


