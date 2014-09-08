import sys
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import nltk
# Setting the encoding as utf-8
reload(sys)
sys.setdefaultencoding("utf-8")
cachedStopWords = set(stopwords.words("english"))
cachedStopWords.add("htm")
cachedStopWords.add("html")

def getHtml(path):
	try:
		file = open(path,"r")
	except Exception, e:
		return ""

	out = nltk.clean_html(file.read())
	file.close()

	return out

# def getHtml(path):
	# try:
	# 	file = open(path,"r")
	# except Exception, e:
	# 	return ""
	
	# html = file.read()
	# file.close()

# 	soup = BeautifulSoup(html)
# 	# kill all script and style elements
# 	for script in soup(["script", "style"]):
# 		script.extract()    # rip it out
# 	# get text
# 	text = soup.get_text()
# 	# break into lines and remove leading and trailing space on each
# 	return text
	 

def getTokenListFromHtml(path):
    inp = getHtml(path)
    tokenizer = RegexpTokenizer(r'\w+')
    return [x.lower() for x in tokenizer.tokenize(inp)]

def getStemmedWords(list):
    stemmer=PorterStemmer()
    return [stemmer.stem(x) for x in list]

def removeStopWords(list):
	return [word for word in list if word not in cachedStopWords]






