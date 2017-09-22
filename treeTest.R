#Elizabeth E. Esterly
#Last revision 09/21/2017
#treeTest.R


library(tidyverse)
source("util.R")
args <- commandArgs(trailingOnly = TRUE)
#read training data
training <- read_csv(args[1], col_names = FALSE)
View(training)
#add dummy column to mimic raw data before features from book data
#for ANY data, ensure that classification result is in the last column!
#if (args[1] == "weatherTraining.csv"){
#  add_column(training, a = 0, .before = "Outlook" )
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

# now get the info gain for each attribute (position) 
# POSITION   INFO GAIN



#example for indexing into dataframe: get the 7th char of the second entry
str_sub(training$X2[2], 7, 7)

#the highest gain is the root of the tree
#makeRoot
#

