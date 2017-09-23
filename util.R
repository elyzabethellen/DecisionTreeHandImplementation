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
    occurences[i] <- sum(d == outcomes[i]) #count number of occurences of each factor
  }
  s <- 0
  for(j in 1 : categories){
    val <- occurences[j]
    s <- s + (-1* val/ totalEntries) * log2(val / totalEntries)
  }
  return(s)
}

##########infoGain#############

#returns information gain you get from using feature as your tree split (bits)
#dEnt     :: dataset entropy
#col      :: column data
#uniques  :: list of unique values from column
#outcomes :: list of classes/classifications
#totalEntries ::length of column
infoGain <- function(dEnt, c, uniques, outcomes, totalEntries, class){
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

infoWrapper <- function(training, dEnt, totalEnt, idx){
  bestGain<- 0
  bestFeat <- NULL
  for(i in (idx + 1) : length(training)){
    c <- select(training, i:i)
    n <- colnames(c)
    uniques <- unique(c[[1]])
    totalEnt <- length(c)
    i <- infoGain(dEnt, c, uniques, outcomes, totalEnt, training$Class)
    if (i > bestGain) {
      bestGain <- i
      bestFeat <- n
    }
  }
  return(c(bestGain, bestFeat))
}


