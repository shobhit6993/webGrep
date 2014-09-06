import html2text
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

# def getHtml(path):
#     h = html2text.HTML2Text()
#     h.ignore_links = True
#     h.ignore_images = True
#     file = open(path, "r")
#     inp = file.read()
#     inp = unicode(inp, errors='ignore')
#     return h.handle(inp)
def getHtml(path):
	file = open(path,"r")
	inp = file.read()
	file.close()
	return nltk.clean_html(inp)

def getTokenListFromHtml(path):
    inp = getHtml(path)
    tokenizer = RegexpTokenizer(r'\w+')
    return [x.lower() for x in tokenizer.tokenize(inp)]

def getStemmedWords(list):
    stemmer=PorterStemmer()
    return [stemmer.stem(x) for x in list]

def removeStopWords(list):
	return [word for word in list if word not in cachedStopWords]






