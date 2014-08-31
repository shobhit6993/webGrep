# populate keys of the dictionary
# for a particular tokenlist
def populateKeysForAFile(indexMap, tokenList):
	for token in tokenList:
		indexMap[token] = []

def getTokens(fileName):
	f = open(fileName, "r")
	s = f.read()
	f.close()
	return s.split()

def populateKeys(indexMap, fileList):
	for fileName in fileList:
		tokenList = getTokens(fileName)
		populateKeysForAFile(indexMap, tokenList)

def returnKeyList(indexMap):
	keyList = []
	for key, value in indexMap.iteritems():
		keyList.append(key)
	return keyList

def returnBatchMap(start, keyList):
	end = min(start+2000, len(keyList))
	batchList = keyList[start:end]
	return {word : "" for word in batchList}

#TODO: have to tweak docId, right now its the filename
def buildPostingList(batchMap, indexMap, fileList):
	for fileName in fileList:
		tokenList = getTokens(fileName)
		postingMap = {}
		pos = 0
		for token in tokenList:
			if batchMap.has_key(token):
				if postingMap.has_key(token):
					postingMap[token].append(pos)
				else:
					postingMap[token] = [pos]
			pos += 1

		for word in postingMap:
			indexMap[word].append([fileName, postingMap[word]])

if __name__ == "__main__":
	indexMap = {}
	fileList = []
	for i in xrange(0,9999):
		fileList.append("./dataset/0/"+str(i))# = ['dummy1.txt', 'dummy2.txt']
	populateKeys(indexMap, fileList)
	# print indexMap
	# print returnVocab(indexMap);
	keyList = returnKeyList(indexMap)

	for start in xrange(0,len(keyList),2000):
		batchMap = returnBatchMap(start, keyList)
		buildPostingList(batchMap, indexMap, fileList)
	
	print len(indexMap)




