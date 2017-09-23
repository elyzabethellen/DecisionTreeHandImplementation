#Elizabeth E. Esterly
#Last revision 09/22/2017
#treeTest.R

library(tidyverse)
library(stringr)
source("util.R")

args <- commandArgs(trailingOnly = TRUE)
#read training data
#training <- read_csv(args[1], col_names = FALSE)
#numFeatures <- args[2]
training <- read_csv("weatherTraining.csv")
#!!!!!!!!!!!!!!!!!!!!!!!!
#?????????????
View(training)

#!!!!!!UNCOMMENT IF USING weathertraining.csv with launcher script
#add dummy column to mimic raw data before features from book data
#for ANY data, ensure that classification result is in the last column!
#if (args[1] == "weatherTraining.csv"){
 #add_column(training, a = 0, .before = "Outlook" )
#}#

#----------------------------------------------------------------#
#!!!!!!!feature extraction and pre-processing section!!!!!!!!!!!!
# call Danny's feature extraction methods and append as columns
# with values of the feature for each one
# then store a quick access data structure 
# with what the info gain is for each data point for
# each feature 
#---i.e., for our features
# call first letter
# call last letter
# call frequencyOfAppearance
# call permutations
totalEntries <- nrow(training)

#calculate entropy of data set
outcomes <- unique(training$Class)
dEnt <- datasetEntropy(training$Class, outcomes, totalEntries)
cat("Dataset Entropy = ",dEnt)
cat("Column names check = ", colnames(training))

#for weather set
# now get the info gain for each attribute and store it
cnames <- colnames(training)
idx <- which(cnames == 'Class')
infoz <- numeric(ncol(training) - idx)
idx <- idx + 1
pos <- 1
for(i in idx : length(training)){
  c <- select(training, i:i)
  uniques <- unique(c[[1]])
  print(uniques)
  totalEnt <- length(c)
  infoz[pos] <- infoGain(dEnt, c, uniques, outcomes, totalEnt, training$Class)
  pos <- pos + 1
}
print(infoz)

#infoz <- apply(subDat, 2, infoGain) 
#print(infoz)



#the highest gain is the root of the tree
#makeRoot


