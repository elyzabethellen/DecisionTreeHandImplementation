# different helpers we found useful for our experiments 

def buildWhiteList(specialKeys,prewhitelist,keys):
	d = {}
	whitelist = list(set(prewhitelist) | (set(keys) - set(specialKeys)))
	return whitelist