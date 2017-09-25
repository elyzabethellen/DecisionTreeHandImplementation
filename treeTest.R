#Elizabeth E. Esterly
#Last revision 09/24/2017
#treeTest.R

library(tidyverse)
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

#make root node 
r <- new("root")

#----------------begin recursive tree-builder function
tree = treeBuilder(PVAL, root, copiedTraining, 1)
print(tree)




