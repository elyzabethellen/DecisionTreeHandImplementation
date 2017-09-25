#Elizabeth E. Esterly, Danny Byrd
#Last revision 09/24/2017
#util.R
#function library script


##########chiSquaredTest#######
# self contained chi squared test to check if a split on a dataset is statistically signifcant 
#data = data set (or subset) to test
#splitAttribute :: (the attribute to test)
#predictionAttribute :: (the attribute which is being predicted) 
#confidenceLevel :: lower bound on the probability of statistical significance for the chi squared statistic 

chiSquaredTest <- function(data,splitAttribute,predictionAttribute,confidenceLevel){

  uniqueSplitValues <- unique(data[splitAttribute])
  uniqueAttributeValues <- unique(data[predictionAttribute])

  splitAttributeCategories <- length(unique(data[splitAttribute])[[1]])
  predictionAttributeCategories <- length(unique(data[predictionAttribute])[[1]])

  degreesFreedom <- (splitAttributeCategories - 1) * (predictionAttributeCategories - 1)

  totalSubsetLength = length(data[[1]])

  chiSquared <- 0

  for (attributeV in uniqueSplitValues[[1]]) {    
      for (predictionV in uniqueAttributeValues[[1]]) {

        av <- sum(data[splitAttribute] == attributeV)
        pv <- sum(data[predictionAttribute] == predictionV)
        expectedValue <- av * pv / totalSubsetLength  
        realValue <- sum(data[splitAttribute] == attributeV & data[predictionAttribute] == predictionV)        
        chiSquared <- chiSquared + ((realValue - expectedValue)^2)/expectedValue
      
      }
  }

  
  if(qchisq(confidenceLevel, df=degreesFreedom)<chiSquared){
    return (TRUE)
  }

  return (FALSE)

}

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
infoGain <- function(training, dEnt, totalEnt, outcomes){
  bestGain<- 0
  bestFeat <- NULL
  idx <- which(colnames(training) == "Class")
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
giniIndex <- function(d, outcomes){
  bestGiniScore <- Inf
  bestGiniName <- NULL
  lowestFeatScore <- Inf
  lowestFeatName <- NULL
  idx <- which(colnames(d) == "Class")
  for(i in (idx + 1) : length(d)){
    c <- select(d, i:i)
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
        g <- g - ((sum(c == uniques[u] & d$Class == outcomes[j])) / t) ^ 2
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

treeBuilder <-function(pVal, n, d, depth){
  cat("In treeBuilder at depth ", depth)
  #first check to see if all Class vals are the same--then we're at a leaf and we're done
  testData <- d["Class"]
  if(length(unique(testData[[1]])) == 1) {
    print("Just one Class remains...sending up a leaf")
    l <- new("leaf")
    l@consenVal <- list(consen(d, testData))
    return()
  }else{
    
    # choose the split by infogain (higher val is better) or gini index (lower val is better)
    #----------------------------------------------------------------
    # (infoGain() calls infoG() on all remaining cols after Class)
    # splitChoice is a list: (infoGainVal, "feature col name")
    if (USEINFOGAIN == TRUE){
      print("info gain used")
      splitChoice <- infoGain(d, dEnt, totalEnt,outcomes)
      #infoGain will now split on all values of the features here, so the split may be non-binary
      #(more than 2 children).
      firstSplitIdx <- which(colnames(d) == splitChoice[2])
      #is this split significant? 
      
      
      #!!!!!!!!!!!!!!!!!!------------- Call Chi-squared----------------!!!!!!!!!!!!!!!!!!!!!!
      print("HEY DUDEEEE")
      
      
      #if it is,
      #grab unique vals from col given in list, 
      #partition data and create nodes; 
      #recurse on those nodes
      
      
      #else create a leaf with consensus val and return
      
    }else{
      # gini index. run on all features and find the lowest val == best column to split on.
      # splitChoice is a list: 
      # (bestcolginiIndexVal, "best feature col name", best subfeature score, "Subfeature Name")
      print("Gini index used")
      splitChoice <- giniIndex(d, outcomes)
      cat("splitChoice value is ", splitChoice[4], "\n")
      #is this split significant? 
      
      
      #!!!!!!!!!!!!!!!!!!------------- Call Chi-squared----------------!!!!!!!!!!!!!!!!!!!!!!
      
      
      #if it is,
      #GINI will implement a binary split partitioning the best scored subfeature value from the remaining values 
      # i.e. in weather book example, first split would partition 1) OVERCAST // 2) SUNNY, RAIN
      #get parent column to split on
      getCol <- d %>% select(splitChoice[2])
      #now split on features; have to pipe in the column so it doesn't string match instead of element matching
      #left will always be the split chosen by GINI
      left <- d %>% filter(getCol == splitChoice[4])
      print("LEFT!")
      print(left)
      
      
      l <- new("node")
      l@name <- paste(splitChoice[2], splitChoice[4], sep = " ")
      
      #right is the other features lumped together
      right <- d %>% filter(getCol != splitChoice[4])
      print("RIGHT!")
      print(right)
      
      
      r <- new("node")
      r@name <- paste(splitChoice[2], "not", splitChoice[4], sep = " ")
      
      #mark these as children of the current node and recurse on both, increasing depth and using limited dataset
      #can't do this by reference--work it out later
      #n@children <- c(l, r)
      cat("The Gini children are created at depth ", depth, "\n")
      treeBuilder(pVal, l, left, depth + 1)
      treeBuilder(pVal, r, right, depth + 1)
      
      #else create a leaf with consensus val and return
    }
  }
}

#############consen######################
#returns the consensus value for Classification.
#data            :: the general data
#col             :: a column of that data
consen <- function(data, Class){
  ##don't forget about that nested tibble indexing here, i.e.:
  ###> b[[1]]
  #>>>>>"Yes"
  print("consen function--leaf found")
  b <- subset(count(data, Class), Class == max(Class))
  return(b[[1]])
}
