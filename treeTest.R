#Elizabeth E. Esterly
#Last revision 09/22/2017
#treeTest.R

library(tidyverse)
source("util.R")

args <- commandArgs(trailingOnly = TRUE)
#read training data
training <- read_csv("weatherTraining.csv")
totalEntries <- nrow(training)

#calculate entropy of data set
outcomes <- unique(training$Class)
dEnt <- datasetEntropy(training$Class, outcomes, totalEntries)

#start subset with class
idx <- which(colnames(training) == 'Class')

# choose the split (infoWrapper() calls infoGain() on all remaining cols after Class)
splitChoice <- infoWrapper(training, dEnt, totalEnt, idx)
print(splitChoice)

#if splitChoice[1] < whatever because of chi-squared, then we stop here and assign all rem data points to majority rule
#else



