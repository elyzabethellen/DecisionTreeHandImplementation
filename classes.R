#class file

root <- setClass(
  "root", 
  slots = c(name = "character", children = "list")
)

#setting parent to list type for easiness even though it's a single object, it could be a root or a node
node <- setClass(
  "node",  
  slots = c(name = "character", children = "list")
)

#setting parent and consenVal to list type for easiness even though it's a single object, 
#it could be a root or a node in parent case or numeric, char, anything in consenVal case
leaf <- setClass(
  "leaf", 
  c = (consenVal = "list")
  )