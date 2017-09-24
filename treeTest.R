#Elizabeth E. Esterly
#Last revision 09/22/2017
#treeTest.R

library(tidyverse)
source("util.R")
source("classes.R")

#IF FALSE THEN GINI INDEX WILL BE USED
USEINFOGAIN <- FALSE

args <- commandArgs(trailingOnly = TRUE)
#read training data
training <- read_csv("weatherTraining.csv")
totalEntries <- nrow(training)

#calculate entropy of data set
outcomes <- unique(training$Class)
dEnt <- datasetEntropy(training$Class, outcomes, totalEntries)

#start subset of data with class column--we'll need to refer to it.
idx <- which(colnames(training) == 'Class')

#make root node 
ID3root <- new("root")
#make new tree
ID3tree <- new("id3tree", children = c(ID3root))
print(ID3tree)


##-----for Debug
View(copiedTraining)

#copy the training data as we will start to delete rows and columns as we use features
#and make classifications
copiedTraining <- training

#----------------begin  tree-builder


#treeBuilder(ID3tree, copiedTraining)
#

#make a test for splitting on the first Gini choice, Outlook for weather set

# choose the split by infogain or gini index
#----------------------------------------------------------------
# (infoGain() calls infoG() on all remaining cols after Class)
# splitChoice is a list: (infoGainVal, "feature col name")
# higher value for info gain is better
if (USEINFOGAIN == TRUE){
  splitChoice <- infoGain(copiedTraining, dEnt, totalEnt, idx, outcomes)
  #infoGain will now split on all values of the features here, so the split may be non-binary
  #(more than 2 children).
  firstSplitIdx <- which(colnames(copiedTraining) == splitChoice[2])
  #grab unique vals partition data and create nodes
  
}else{
  # gini index. run on all features and find the lowest val == best column to split on.
  # splitChoice is a list: 
  # (bestcolginiIndexVal, "best feature col name", best subfeature score, "Subfeature Name")
  splitChoice <- giniIndex(copiedTraining, idx, outcomes)
  #GINI will implement a binary split partitioning the best scored subfeature value from the remaining values 
  # i.e. in weather book example, first split would partition OVERCAST // SUNNY, RAIN
}

#level <- level + 1
#}
  
testConsensus <- consen(copiedTraining, copiedTraining$Class)
print(testConsensus)


