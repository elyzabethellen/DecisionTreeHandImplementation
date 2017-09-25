#Elizabeth E. Esterly, Danny Byrd
#Last revision 09/25/2017
#treeTest.R

library(tidyverse)
require(tidyverse)
source("util.R")
source("classes.R")

#THESE WILL COME IN IN SCRIPT
#IF FALSE THEN GINI INDEX WILL BE USED
USEINFOGAIN <- FALSE
PVAL <- 0.95

args <- commandArgs(trailingOnly = TRUE)
#read training data
training <- read_csv("weatherTraining.csv")
totalEntries <- nrow(training)

#calculate entropy of data set
outcomes <- unique(training$Class)
dEnt <- datasetEntropy(training$Class, outcomes, totalEntries)

#copy the training data as a backup as we will start to do a ton of operations on it
copiedTraining <- training

#----------------begin recursive tree-builder function
tree = buildTree(PVAL, copiedTraining, 1)
print(tree)




