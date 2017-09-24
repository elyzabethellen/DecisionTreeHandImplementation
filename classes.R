#class file

Root <- setClass(
  "root", 
  representation =list(
    children = "list"
    ),
  contains = "NULL"
)

#setting parent to list type for easiness even though it's a single object, it could be a root or a node
Node <- setClass(
  "node",  
  representation = list(
    children = "list"
  ),
  contains = "NULL"
)

#setting parent and consenVal to list type for easiness even though it's a single object, 
#it could be a root or a node in parent case or numeric, char, anything in consenVal case
Leaf <- setClass(
  "leaf", 
  representation = list( 
      consenVal = "list"
      ),
  contains = "NULL"
  )