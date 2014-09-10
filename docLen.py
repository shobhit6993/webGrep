docLenMapFile = "DocLenMap"
noOfFiles = 100
stFlr = 0
enFlr = 0

def readDocLenMap():
	fileObj = open(docLenMapFile, "rb")
	strList = fileObj.read()
	fileObj.close()

	docLenMap = {}
	arr = strList.split(",")
	# print arr
	for element in arr:
		if element == '':
			break

		pair = element.split(":")
		docLenMap[int(pair[0])] = int(pair[1])
	return docLenMap

def buildDocLenMap():
	docLenMap = {}
	for flr in xrange(stFlr,enFlr+1):
		if flr == 3: continue
		for i in xrange(0, noOfFiles):
				fileObj = open("./dataset/"+ str(flr)+"/"+str(flr*noOfFiles+i),"ab")
				# print  str(flr*noOfFiles+i)
				docLenMap[flr*noOfFiles+i] = int(fileObj.tell())
				fileObj.close()
	return docLenMap

def dumpDocLenMap(docLenMap):
	strList = []
	for key in docLenMap:
		strList.append(str(key) + ":"+str(docLenMap[key])+",")
	# strList.append("$")
	stringToDump = ''.join(strList)
	fileObj = open(docLenMapFile, "wb")
	fileObj.write(stringToDump)
	fileObj.close()

	
if __name__ == "__main__":
	docLenMap = buildDocLenMap()
	# print docLenMap
	dumpDocLenMap(docLenMap)
	print readDocLenMap()
	
