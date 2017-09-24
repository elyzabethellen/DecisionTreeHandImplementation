#Elizabeth E. Esterly
#Last revision 09/22/2017
#util.R
#function library script

##########datasetEntropy#######
#returns entropy s of dataset column vector d
#d    :: dataset

datasetEntropy <- function(d, outcomes, totalEntries){
  categories <- length(outcomes)
  
  #makes vector of zeroes of length categories
  occurences <- integer(categories)
  for(i in 1 : categories){
    #count number of occurences of each factor
    occurences[i] <- sum(d == outcomes[i]) 
  }
  s <- 0
  for(j in 1 : categories){
    val <- occurences[j]
    s <- s + (-1* val/ totalEntries) * log2(val / totalEntries)
  }
  return(s)
}

##########infoG#############
#does the heavy lifting for infoGain()
#returns information gain you get from using feature as your tree split (bits)
#dEnt     :: dataset entropy
#col      :: column data
#uniques  :: list of unique values from column
#outcomes :: list of classes/classifications
#totalEntries ::length of column
infoG <- function(dEnt, c, uniques, outcomes, totalEntries, class){
  #for each unique value in col find how many occurences
  x <- 0
  for(i in 1 : length(uniques)){
    g <- 0
    t <- sum(c == uniques[i])
    
    #loop for outcomes, eg classes
    for(j in 1 : length(outcomes)){
      classCount <- sum(c == uniques[i] & class == outcomes[j])
      if (classCount != 0) { g <- g + (-1* classCount / t) * log2( classCount / t)}
      else{g <- g + 0}
    }
   x <- (t / nrow(c)) * g + x
  }
  return(dEnt - x)
}

##########infoGain#############
#returns best (information gain, "feature col name")
#training :: dataset
#dEnt     :: dataset entropy
#idx      :: index of column to begin evaluating from
#totalEnt ::length of column
# outcomes:: vector of unique classes (e.g. ("Yes", "No"))
infoGain <- function(training, dEnt, totalEnt, idx, outcomes){
  bestGain<- 0
  bestFeat <- NULL
  for(i in (idx + 1) : length(training)){
    c <- select(training, i:i)
    n <- colnames(c)
    uniques <- unique(c[[1]])
    totalEnt <- length(c)
    i <- infoG(dEnt, c, uniques, outcomes, totalEnt, training$Class)
    if (i > bestGain) {
      bestGain <- i
      bestFeat <- n
    }
  }
  return(c(bestGain, bestFeat))
}

##########giniIndex#############
#training :: dataset
#idx      :: index of column to begin evaluating from
# outcomes:: vector of unique classes (e.g. ("Yes", "No"))
giniIndex <- function(training, idx, outcomes){
  bestGiniScore <- Inf
  bestGiniName <- NULL
  lowestFeatScore <- Inf
  lowestFeatName <- NULL
  for(i in (idx + 1) : length(training)){
    c <- select(training, i:i)
    n <- colnames(c)
    
    #get unique feature values for this column
    uniques <- unique(c[[1]])
    l <- nrow(c)
    acc <- 0
    lowest <- Inf
    lowestN <- NULL
    #for each unique value for a feature, 
    for (u in 1: length(uniques)){
      #how many are here total?
      t <- sum(c == uniques[u])
      g <- 1
      #eval Gini index and store name if it's the best
      for (j in 1: length(outcomes)){
                   #how many match a certain outcome?
        g <- g - ((sum(c == uniques[u] & training$Class == outcomes[j])) / t) ^ 2
      }
      g <- g * (t / l) 
      # store ind scores here too to return for the split.
      if (g < lowest){
        lowest <- g
        lowestN <- uniques[u]
      }
      acc <- acc + g
    }
    if (acc < bestGiniScore){
      bestGiniScore <- acc
      bestGiniName <- n
      lowestFeatScore <- lowest
      lowestFeatName <- lowestN
    }
  }
  return(c(bestGiniScore, bestGiniName, lowestFeatScore, lowestFeatName))
}

##################treeBuilder################
#pVal               ::critical value for split stopping

treeBuilder <-function(pVal, copiedTraining){
  if((chiSquare() < pVal) | length(unique(copiedTraining$Class)) == 1) {
    
    return(makeLeaf(copiedTraining$Class))
  }else{
    
  }

}
