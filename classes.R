#class file

setClass(
  "Root", 
  representation(
    children = "list"
    ),
  contains = c("NULL", "character")
)

#setting parent to list type for easiness even though it's a single object, it could be a root or a node
setClass(
  "Node",  
  representation(
    name = "character",
    children = "list"
  ),
  contains = c("NULL", "character")
)

#setting parent and consenVal to list type for easiness even though it's a single object, 
#it could be a root or a node in parent case or numeric, char, anything in consenVal case
setClass(
  "Leaf", 
  representation( 
      consenVal = "list"
      ),
  contains = c("NULL", "character")
  )