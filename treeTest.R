#Elizabeth E. Esterly
#Last revision 09/10/2017
#treeTest.R
#predict: play == yes

library(readr)
source("util.R")

args <- commandArgs(trailingOnly = TRUE)
#read training data
training <- read_csv(args[1])
#print to console
print(training)

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
