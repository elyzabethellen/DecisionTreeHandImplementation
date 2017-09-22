#class file

setClass("root", slots = list(children = "list"))
setClass("node", slots = list(children = "list", parent = "list"))
setClass("leaf", slots = list(parent = "list"))