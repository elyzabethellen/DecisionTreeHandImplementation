#Elizabeth E. Esterly
#Last revision 09/10/2017
#treeTest.R
#predict: play == yes

library(tidyverse)
source("util.R")


args <- commandArgs(trailingOnly = TRUE)
#read training data
training <- read_csv(args[1])
#add dummy column to mimic raw data before features from book data
#for ANY data, ensure that classification result is in the last column!
if (args[1] == "weatherTraining.csv"){
  add_column(training, a = 0, .before = "Outlook" )
}

#----------------------------------------------------------------#
# feature extraction and pre-processing
# call Danny's feature extraction methods and append as columns
# with values for what the info gain is for each data point for
# each feature 

#---i.e., for our features
# call first letter
# call last letter
# call frequencyOfAppearance
# call permutations

#--for the book features the fields are already populated


#now get the info gain for each feature and store as a tuple, sort by the highest gain.
#Gain(S, Outlook) = 0.246
#Gain(S, Temperature) = 0.029
#Gain(S, Humidity) = 0.151
#Gain(S, Wind) = 0.048 


#calculate entropy of data set
#Entropy(S) = 0.940286
#dEnt <- datasetEntropy(training$Play, c("Yes", "No"))
outcomes <- unlist(strsplit(args[3], ","))
#---------Not sure yet how to get the Play column in as a variable, it won't read as a command arg
dEnt <- datasetEntropy(training$Play, outcomes)
cat("Dataset Entropy = ",dEnt)



#the highest gain is the root of the tree
