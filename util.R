#Elizabeth E. Esterly
#Last revision 09/21/2017
#util.R
#function library script

##########datasetEntropy#######
#takes dataset d
#returns entropy s of dataset column vector d
datasetEntropy <- function(d, vars){
  totalEntries <- length(d)
  categories <- length(vars)
  occurences <- integer(categories)
  for(i in 1 : categories){
    occurences[i] <- sum(d == vars[i]) #count number of occurences of each factor
  }
  s <- 0
  for(j in 1 : categories){
    val <- occurences[j]
    s <- s + (-1* val/ totalEntries) * log2(val / totalEntries)
  }
  return(s)
}

##########infoGain#############
#takes x
#returns information gain g you get from using feature x as your tree split (bits)
infoGain <- function(x){
  g <- NULL
  return(g)
}