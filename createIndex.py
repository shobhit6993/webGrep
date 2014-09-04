import cPickle
import tokenizer

# def tokenize(fileObj):
# 	s = fileObj.read()
# 	return s.split()

def increaseFileSize(slabSize):
	fileObj = open("PostingList","ab")
	retVal = fileObj.tell()
	print retVal
	for i in xrange(0,slabSize):
		fileObj.write('0')
	fileObj.close()
	return retVal

def buildIndexMapAndPosList(keyList, indexMap, slabSize, lastOffset, posList):
	i = 0
	# posList = {}
	for key in keyList:
		if not indexMap.has_key(key):
			indexMap[key] = lastOffset
			lastOffset += slabSize
			
		if not posList.has_key(key):
			posList[keyList[i]] = [i]
		else:
			posList[keyList[i]].append(i)

		i += 1
	# print posList
	return lastOffset

def dumpIndexMap(indexMap):
	cPickle.dump(indexMap, open("OffsetMap", "wb"))

def readIndexMap():
	return cPickle.load(open("OffsetMap", "rb"))

def mergePostingList(postingListForABatch, indexMap, slabSize, bookKeeping, lastDump):
	fileObj = open("PostingList", "r+b")
	for key in postingListForABatch:	
		if lastDump.has_key(key):
			try:
				fileObj.seek(lastDump[key], 0)
				book = fileObj.read(bookKeeping).split('$')
				fileContent = fileObj.read(slabSize - bookKeeping)
				postingListForAWord = cPickle.loads(fileContent)
				postingListForAWord += postingListForABatch[key]
				dumpString = cPickle.dumps(postingListForAWord)
				print str(book[1]) + " " + str(len(dumpString))
				if len(dumpString) + bookKeeping  < slabSize:
					fileObj.seek(lastDump[key], 0)
					fileObj.write(str(-1) + "$" + str(len(dumpString)) + "$")
					fileObj.seek(lastDump[key] + bookKeeping, 0)
					fileObj.write(dumpString)
				else:
					print lastDump[key]
					fileObj.seek(lastDump[key], 0)
					lastDump[key] = increaseFileSize(slabSize)
					print lastDump[key]
					fileObj.write(str(lastDump[key]) + "$" + book[1] + "$")
					postingListForAWord = postingListForABatch[key]
					dumpString = cPickle.dumps(postingListForAWord)
					fileObj.seek(lastDump[key], 0)
					fileObj.write(str(-1) + "$" + str(len(dumpString)) + "$")
					fileObj.seek(lastDump[key] + bookKeeping, 0)
					fileObj.write(dumpString)
			except (EOFError,cPickle.UnpicklingError):
				continue
		else:
			increaseFileSize(slabSize)
			lastDump[key] = indexMap[key]
			postingListForAWord = postingListForABatch[key]
			dumpString = cPickle.dumps(postingListForAWord)
			fileObj.seek(lastDump[key], 0)
			fileObj.write(str(-1) + "$" + str(len(dumpString)) + "$")
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
	fileObj = open("PostingList", "rb")
	for key in indexMap:
		fileObj.seek(indexMap[key]+bookKeeping, 0)
		try:
			print cPickle.load(fileObj)
		except(EOFError,cPickle.UnpicklingError):
			continue
	
	fileObj.close()	
	

if __name__ == "__main__":
	fileObj = open("PostingList","wb")
	fileObj.close()
	# Tokenising the files to get a keyList
	keyList = []
	indexMap = {}
	bookKeeping = 50
	slabSize = 10000 + bookKeeping
	lastOffset = 0
	lastDump = {}
	for i in xrange(0, 2):
		postingListForABatch = {}
		for j in xrange(0, 1):
			# fileObj = open("./dataset/" + str(i) + "/" + str(j+50*i), "rb")
			# keyList = tokenize(fileObj)`1
			keyList = tokenizer.getTokenListFromHtml("./dataset/" + str(i) + "/" + str(j))
			# fileObj.close()
			postingListForAFile = {}
			lastOffset = buildIndexMapAndPosList(keyList, indexMap, slabSize, lastOffset, postingListForAFile)
			buildPostingListForABatch(postingListForABatch, postingListForAFile, i)
			print "|keyList| = " + str(len(keyList))
			print str(j) + "done"
		mergePostingList(postingListForABatch, indexMap, slabSize, bookKeeping, lastDump)
		#print postingListForABatch
	# Dumping the index into a file
	dumpIndexMap(indexMap)

	#readPostingFile(indexMap)
