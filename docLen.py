docLenListFile = "DocLenList"
noOfFiles = 10000
stFlr = 0
enFlr = 1

def readDocLenList():
	fileObj = open(docLenListFile, "rb")
	strList = fileObj.read()
	fileObj.close()

	docLenList = []
	arr = strList.split(",")
	# print arr
	for element in arr:
		if element == '':
			break

		docLenList.append(int(element))
	return docLenList

def buildDocLenList():
	docLenList = []
	for flr in xrange(stFlr,enFlr+1):
		if flr == 3: continue
		for i in xrange(0, noOfFiles):
				fileObj = open("./dataset/"+ str(flr)+"/"+str(flr*noOfFiles+i),"ab")
				# print  str(flr*noOfFiles+i)
				docLenList.append(int(fileObj.tell()))
				fileObj.close()
	return docLenList

def dumpDocLenList(docLenList):
	strList = []
	for elem in docLenList:
		strList.append(str(elem)+",")
	# strList.append("$")
	stringToDump = ''.join(strList)
	fileObj = open(docLenListFile, "wb")
	fileObj.write(stringToDump)
	fileObj.close()

	
if __name__ == "__main__":
	docLenList = buildDocLenList()
	# print docLenList
	dumpDocLenList(docLenList)
	# print readDocLenList()
	
