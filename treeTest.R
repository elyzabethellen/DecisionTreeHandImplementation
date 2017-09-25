#Elizabeth E. Esterly
#Last revision 09/24/2017
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

#copy the training data as a backup as we will start to do a ton of operations on it
copiedTraining <- training

#make root node 
root <- new("Root", children <- c("empty"))
f <- new("Node", name <- "f", children <- c("empty"))
g <- new("Node", name <- "g", children <- c("empty"))
root@children <- c(f,g)
print(root@children)

#----------------begin recursive tree-builder function
#tree = treeBuilder(pVal, root, copiedTraining, 1)
#print(tree)




