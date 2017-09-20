#Elizabeth E. Esterly
#Last revision 09/10/2017
#treeTest.R
#predict: play == yes

library(tidyverse)
source("util.R")


args <- commandArgs(trailingOnly = TRUE)
#read training data
training <- read_csv(args[1])
#add dummy column to mimic raw data before feature extraction from book data
if (args[1] == "weatherTraining.csv"){
  add_column(training, a = 0, .before = "Outlook" )
}

#----------------------------------------------------------------#
# feature extraction
# call Danny's feature extraction methods and append as columns
# create a vector of what the info gain is for each feature and pair with 
###the name of that feature



#--------deal with NAs and NANs here in more complex datasets----#

#calculate entropy of data set
#Entropy(S) = 0.940286
#dEnt <- datasetEntropy(training$Play, c("Yes", "No"))
outcomes <- unlist(strsplit(args[3], ","))
#---------Not sure yet how to get the Play column in as a variable, it won't read as a command arg
dEnt <- datasetEntropy(training$Play, outcomes)
cat("Dataset Entropy = ",dEnt)

#---------get args for attribute vector? Probably-------------------------#
#calculate info gain for all attributes at the outset.


#Gain(S, Outlook) = 0.246

#Gain(S, Temperature) = 0.029

#Gain(S, Humidity) = 0.151

#Gain(S, Wind) = 0.048 

#the highest gain is the root of the tree
