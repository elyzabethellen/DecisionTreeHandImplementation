#class file

ID3Tree <- setClass(
  "id3tree",
  slots = c(
    children = "list"
  ),
  prototype = list(
    children = c()
  )
)

Root <- setClass(
  "root", 
  slots = c(
    children = "list"
    ),
  prototype = list(
    children = c()
  )
)

#setting parent to list type for easiness even though it's a single object, it could be a root or a node
Node <- setClass(
  "node", 
  slots = c(
    children = "list", 
    parent = "list"),
  prototype = list(
    children = c(),
    parent = c()
  )
  )

Leaf <- setClass(
  "leaf", slots = 
    c(
      parent = "list"
      ),
  prototype = list(
    parent = c()
  )
  )