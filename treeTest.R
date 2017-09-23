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

#if all the class members are of 1 type, we're done. else:


# choose the split by infogain or gini index
#----------------------------------------------------------------
# (infoGain() calls infoG() on all remaining cols after Class)
# splitChoice is a list: (infoGainVal, "feature col name")
# higher value for info gain is better
if (USEINFOGAIN == TRUE){
  splitChoice <- infoGain(training, dEnt, totalEnt, idx, outcomes)
  
}else{
  # gini index. run on all features and find the lowest val.
  # splitChoice is a list: (giniIndexVal, "feature col name")
  splitChoice <- giniIndex(training, idx, outcomes)
  firstSplitIdx <- which(colnames(training) == splitChoice[2])
}


#make root node 
ID3root <- new("root")
#make new tree
ID3tree <- new("id3tree", children = c(ID3root))
print(ID3tree)

#----------------begin recursive tree-builder
#if all classes are the same or splitChoice[1] < significant val set by chi-squared, 
# then we stop here and assign all 
#rem data points to majority rule leaf
if(length(unique(training$Class)) == 1){
  
}

#else



