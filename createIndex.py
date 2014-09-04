import cPickle

def tokenize(fileObj):
	s = fileObj.read()
	return s.split()

def buildIndexMap(keyList, indexMap, slaSize, lastOffset):
	for key in keyList:
		if not indexMap.has_key(key):
			indexMap[key] = lastOffset
			lastOffset += slaSize

def dumpIndexMap(indexMap):
	cPickle.dump(indexMap, open("OffsetMap", "w"))

def readIndexMap():
	return cPickle.load(open("OffsetMap", "r"))

def createPostingListForAFile(keyList, indexMap):
	posList = {}
	for i in range( 0, len(keyList) ):
		if posList.has_key(keyList[i]):
			posList[keyList[i]].append(i)
		else:
			posList[keyList[i]] = [i]
	
	return posList

def mergePostingList(postingListForAFile, indexMap, docId, slaSize, dumpedOnce):
	fileObj = open("PostingList", "a+")
	for key in postingListForAFile:	
		print dumpedOnce.has_key(key)
		if dumpedOnce.has_key(key): 
			print lskjdflksdlsdjf
			fileObj.seek(indexMap[key], 0)
			try:
				postingListForAWord = cPickle.load(fileObj)
				postingListForAWord.append([docId, postingListForAFile[key]])
			except (EOFError,cPickle.UnpicklingError):
				continue
				
			
		else:
			dumpedOnce[key] = ""
			postingListForAWord = [[docId, postingListForAFile[key]]]
			
		fileObj.seek(indexMap[key], 0)
		cPickle.dump(postingListForAWord, fileObj)
		fileObj.seek(indexMap[key], 0)
		try:
			print cPickle.load(fileObj)
		except(EOFError,cPickle.UnpicklingError):
			continue

	fileObj.close()

def readPostingFile(indexMap):
	fileObj = open("PostingList", "r")
	for key in indexMap:
		#print key
		fileObj.seek(indexMap[key], 0)
		try:
			print cPickle.load(fileObj)
		except(EOFError,cPickle.UnpicklingError):
			continue
	
	fileObj.close()	
	
def testPickle():
	fileObj = open("in", "w+")
	dic = {"aditya":True, "jha":1}
	fileObj.seek(10, 0)
	cPickle.dump(dic, fileObj)
	dic = {}
	fileObj.seek(10, 0)	
	dic = cPickle.load(fileObj)	
	fileObj.close()
	print dic
	
	dic = {}
	fileObj = open("in", "a+")
	fileObj.seek(10, 0)	
	dic = cPickle.load(fileObj)	
	fileObj.close()
	
	print dic	
		
if __name__ == "__main__":
#	testPickle()

	# Tokenising the files to get a keyList
	keyList = []
	indexMap = {}
	slaSize = 100000
	lastOffset = 0
	dumpedOnce = {}
	for i in range(0, 1):
		for j in range(0, 1):
			fileObj = open("./" + str(i) + "/" + str(j), "rb")
			keyList = tokenize(fileObj)
			fileObj.close()
			buildIndexMap(keyList, indexMap, slaSize, lastOffset)
			postingListForAFile = createPostingListForAFile(keyList, indexMap)
			mergePostingList(postingListForAFile, indexMap, j, slaSize, dumpedOnce)
			print "|keyList| = " + str(len(keyList))
	
	# Dumping the index into a file
	dumpIndexMap(indexMap)

	readPostingFile(indexMap)

#	fileObj = open("PostingList", "rb")	
#	postingList = {}
#	for key in indexMap:
#		postingListString = fileObj.read(slaSize)
#		postingList[key] = cPickle.loads(postingListString)
#	print postingList
