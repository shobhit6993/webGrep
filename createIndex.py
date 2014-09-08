import sys
import cPickle
import tokenizer
import threading

postingListFile = ""
offsetMapFile = ""
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
	tempFileObj = open(postingListFile,"ab")
	initialFileEnd = tempFileObj.tell()
	tempFileObj.close()

	fileEnd = initialFileEnd
	fileObj = open(postingListFile, "r+b")
	strList = []
	for key in postingListForABatch:
		size = 0	
		if lastDump.has_key(key):
			try:
				fileObj.seek(lastDump[key], 0)
				postingListForAWord = postingListForABatch[key]
				dumpString = cPickle.dumps(postingListForAWord)
				lastDump[key] = fileEnd
				fileObj.write(str(lastDump[key]) + "$" )
				tempString = str(-1) + "$";
				strList.append(tempString + '0'*(bookKeeping-len(tempString)))
				size += len(strList[-1])
				strList.append(dumpString)
				size += len(strList[-1])
				indexMap[key][1] += len(postingListForAWord)
			except (EOFError,cPickle.UnpicklingError):
				continue
		else:
			postingListForAWord = postingListForABatch[key]
			dumpString = cPickle.dumps(postingListForAWord)
			lastDump[key] = fileEnd
			tempString = str(-1) + "$";
			strList.append(tempString + '0'*(bookKeeping-len(tempString)))
			size += len(strList[-1])
			strList.append(dumpString)
			size += len(strList[-1])
			indexMap[key] = [lastDump[key], len(postingListForAWord)]
		

		fileEnd += size

	fileObj.seek(0,2)
	stringToDump = ''.join(strList)
	fileObj.write(stringToDump)
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

	
	# Tokenising the files to get a keyList
	keyList = []
	indexMap = {}	#indexMap key=word, and value is a list, whose 1st element=offest of posting list in file
					#and second element is the doc freq of that word 
	noOfBatches = 1
	batchSize = 10000
	lastDump = {}
	threads = []

	stFlr = int(sys.argv[1])
	enFlr = int(sys.argv[2])
	exec 'postingListFile="PostingList"+`stFlr`' in globals()
		# postingListFile = "PostingList"+`flr`
	exec 'offsetMapFile="OffsetMap"+`stFlr`' in globals()
	fileObj = open(postingListFile,"wb")
	fileObj.close()
	for flr in xrange(stFlr,enFlr):

		if flr == 3: continue
		for i in xrange(0, noOfBatches):
			postingListForABatch = {}
			for j in xrange(0, batchSize):
				# keyList = tokenizer.getTokenListFromHtml("./dataset/" + str(flr) +"/" + str(flr*10000+batchSize*i+j))
				keyList = tokenizer.getStemmedTokensFromHtml("./dataset/" + str(flr) +"/" + str(flr*10000+batchSize*i+j))
				postingListForAFile = {}
				buildPosList(keyList, postingListForAFile)
				buildPostingListForABatch(postingListForABatch, postingListForAFile, flr*10000+batchSize*i+j)
				# print "|keyList| = " + str(len(keyList))
				print str(flr*10000+batchSize*i+j)

			for t in threads:
				print 'join'
				t.join()

			# t = threading.Thread(target=mergePostingList,args=(postingListForABatch, indexMap, bookKeeping, lastDump,))
			# t.start()
			# threads.append(t);
			mergePostingList(postingListForABatch, indexMap, bookKeeping, lastDump)
			#print postingListForABatch
	# Dumping the index into a file
	for t in threads:
		print 'join'
		t.join()
	dumpIndexMap(indexMap)

	# readPostingFile(indexMap)
	# print readIndexMap()
