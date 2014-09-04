import html2text
import sys
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
# Setting the encoding as utf-8
reload(sys)
sys.setdefaultencoding("utf-8")


def getHtml(path):
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    file = open(path, "r")
    inp = file.read()
    inp = unicode(inp, errors='ignore')
    return h.handle(inp)


def getTokenListFromHtml(path):
    inp = getHtml(path)
    tokenizer = RegexpTokenizer(r'\w+')
    return [x.lower() for x in tokenizer.tokenize(inp)]

def getStemmedWords(list):
    stemmer=PorterStemmer()
    return [stemmer.stem(x) for x in list]

toks = getTokenListFromHtml("/home/harshil/Google.html")
stemtoks = getStemmedWords(toks)





