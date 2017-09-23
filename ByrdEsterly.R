#Elizabeth E. Esterly
#Last revision 09/21/2017
#ByrdEsterly.R


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
  a <- 0
  t <- 0
  c <- 0
  g <- 0
  #for each entry in the training data
  for(r in 1:nrow(training)){
    cat("r = ", r)
    current <- str_sub(training$X2[r], i, i)
    if (current == 'A'){a <- a + 1}
    else if (current == 'T'){t <- t + 1}
    else if (current == 'C'){c <- c +  1}
    else if (current == 'G'){g <- g + 1}
    else {
      feat <- c(a, t, c, g)
      s <- sample(feat, 1) 
      s <- s + 1
    }
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


