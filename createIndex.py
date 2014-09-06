import cPickle
import tokenizer

postingListFile = "PostingList"
offsetMapFile = "OffsetMap"
bookKeeping = 15
# def tokenize(fileObj):
# 	s = fileObj.read()
# 	return s.split()

def increaseFileSize(chunkSize):
	fileObj = open(postingListFile,"ab")
	retVal = fileObj.tell()
	for i in xrange(0,chunkSize):
		fileObj.write('0')
	fileObj.close()
	return retVal

def buildPosList(keyList, posList):
	i = 0
	# posList = {}
	for key in keyList:	
		if not posList.has_key(key):
			posList[keyList[i]] = [i]
		else:
			posList[keyList[i]].append(i)

		i += 1


def dumpIndexMap(indexMap):
	cPickle.dump(indexMap, open(offsetMapFile, "wb"))

# def readIndexMap():
# 	return cPickle.load(open(offsetMapFile, "rb"))

def mergePostingList(postingListForABatch, indexMap, bookKeeping, lastDump):
	fileObj = open(postingListFile, "r+b")
	for key in postingListForABatch:	
		if lastDump.has_key(key):
			try:
				fileObj.seek(lastDump[key], 0)
				postingListForAWord = postingListForABatch[key]
				dumpString = cPickle.dumps(postingListForAWord)
				lastDump[key] = increaseFileSize(len(dumpString) + bookKeeping)
				fileObj.write(str(lastDump[key]) + "$" )
				fileObj.seek(lastDump[key], 0)
				fileObj.write(str(-1) + "$")
				fileObj.seek(lastDump[key] + bookKeeping, 0)
				fileObj.write(dumpString)
				indexMap[key][1] += len(postingListForAWord)
			except (EOFError,cPickle.UnpicklingError):
				continue
		else:
			postingListForAWord = postingListForABatch[key]
			dumpString = cPickle.dumps(postingListForAWord)
			lastDump[key] = increaseFileSize(len(dumpString) + bookKeeping)
			indexMap[key] = [lastDump[key], len(postingListForAWord)]
			fileObj.seek(lastDump[key], 0)
			fileObj.write(str(-1) + "$")
			fileObj.seek(lastDump[key] + bookKeeping, 0)
			fileObj.write(dumpString)

	fileObj.close()

def buildPostingListForABatch(postingListForABatch, postingListForAFile, docId):
	for key in postingListForAFile:
		if not postingListForABatch.has_key(key):
			postingListForABatch[key] = [[docId, postingListForAFile[key]]]
		else:
			postingListForABatch[key].append([docId, postingListForAFile[key]])

def readPostingFile(indexMap):
	fileObj = open(postingListFile, "rb")
	for key in indexMap:
		fileObj.seek(indexMap[key][0]+bookKeeping, 0)
		try:
			print cPickle.load(fileObj)
		except(EOFError,cPickle.UnpicklingError):
			continue
	
	fileObj.close()	

def readIndexMap():
	fileObj = open(offsetMapFile, "rb")
	try:
		return cPickle.load(fileObj)
	except(EOFError,cPickle.UnpicklingError):
		print "error"
	
	fileObj.close()	
	

if __name__ == "__main__":
	fileObj = open(postingListFile,"wb")
	fileObj.close()
	# Tokenising the files to get a keyList
	keyList = []
	indexMap = {}	#indexMap key=word, and value is a list, whose 1st element=offest of posting list in file
					#and second element is the doc freq of that word 
	
	lastDump = {}
	for i in xrange(0, 10):
		postingListForABatch = {}
		for j in xrange(0, 10):
			keyList = tokenizer.getTokenListFromHtml("./dataset/" + str(0) + "/" + str(10*i+j))
			postingListForAFile = {}
			buildPosList(keyList, postingListForAFile)
			buildPostingListForABatch(postingListForABatch, postingListForAFile, 10*i+j)
			# print "|keyList| = " + str(len(keyList))
			print str(10*i+j)
		mergePostingList(postingListForABatch, indexMap, bookKeeping, lastDump)
		#print postingListForABatch
	# Dumping the index into a file
	dumpIndexMap(indexMap)

	# readPostingFile(indexMap)
	# print readIndexMap()
