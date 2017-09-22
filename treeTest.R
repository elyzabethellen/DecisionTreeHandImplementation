#Elizabeth E. Esterly
#Last revision 09/21/2017
#treeTest.R


library(tidyverse)
library(stringr)
source("util.R")
args <- commandArgs(trailingOnly = TRUE)
#read training data
#!!!!!!!!UNCOMMENT FOR TURNIN!!!!!!!!!!
#training <- read_csv(args[1], col_names = FALSE)
#!!!!!!!!!!!!!!!!!!!!!!!!\

##below for testing only!!!!!!!!!
training <- read_csv("training.csv", col_names = FALSE)
#?????????????
View(training)

#!!!!!!UNCOMMENT IF USING weathertraining.csv
#add dummy column to mimic raw data before features from book data
#for ANY data, ensure that classification result is in the last column!
#if (args[1] == "weatherTraining.csv"){
 #add_column(training, a = 0, .before = "Outlook" )
#}

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

#calculate entropy of data set
outcomes <- unique(last(training))
dEnt <- datasetEntropy(last(training), outcomes)
cat("Dataset Entropy = ",dEnt)
cat("Column names check = ", colnames(training))

# now get the info gain for each attribute (position) and store it
# POSITION   INFO GAIN
# let the index be the position, store the info gain there

operations <- 0
numAtts <- 60
print(nrow(training))
#for each attribute (1 - 60)
for (i in 1:numAtts){
  #for each entry in the training data
  for(r in 1:nrow(training)){
    current <- str_sub(training$X2[r], i, i)
    operations <- operations +1
    #count number of A, C, T, G in that position
    #get entropy of A, C, G, T, at that position all the way down the column, so read the char and get the outcome in last
    #last(training)[i]
  }
}
#120000 = 60 * 2000 operations, this is what we would expect. Good
print(operations)


#the highest gain is the root of the tree
#makeRoot


