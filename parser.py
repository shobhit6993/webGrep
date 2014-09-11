import ply.yacc as yacc
from lexer import tokens
import retrieve
import time
from docLen import readDocLenList 

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
	('left', 'QUOTE'),
    ('left', 'LPAREN', 'RPAREN'),
)

rankingMeasure = ""

def p_expression_paren(p):
	'expression : LPAREN expression RPAREN'
	p[0] = p[2]
	
def p_expression_and(p):
	'expression : expression AND expression'
	if rankingMeasure == "tf":	
		p[0] = retrieve.intersectionOfTupleList(p[1], p[3], lambda x, y : min(x, y))
	elif rankingMeasure == "tfidf":
		p[0] = retrieve.intersectionOfTupleList(p[1], p[3], lambda x, y : (x * y)/(x + y))
	
def p_expression_or(p):
	'expression : expression OR expression'
	p[0] = retrieve.unionOfTupleList(p[1], p[3])
	
#def p_expression_not
#	'expression : NOT expression'
	
def p_expression_expterm(p):
	'expression : expression TERM'
	p[2] = p[2].lower()
	if indexMap.has_key(p[2]):
		offset = indexMap[p[2]][0]
		postingListForTerm = retrieve.getPostingList(offset)
		if rankingMeasure == "tf":	
			termTuple = retrieve.convertToTuple(postingListForTerm)
		elif rankingMeasure == "tfidf":
			termTuple = retrieve.convertToTfIdfTuple(postingListForTerm, indexMap[p[2]], len(docLenList))
	else:
		postingListForTerm = []
		termTuple = []

	p[0] = retrieve.unionOfTupleList(p[1], termTuple)
	
def p_expression_term(p):
	'expression : TERM'
	p[1] = p[1].lower()
	if indexMap.has_key(p[1]):
		offset = indexMap[p[1]][0]
		postingListForTerm = retrieve.getPostingList(offset)
		if rankingMeasure == "tf":	
			termTuple = retrieve.convertToTuple(postingListForTerm)
		elif rankingMeasure == "tfidf":
			termTuple = retrieve.convertToTfIdfTuple(postingListForTerm, indexMap[p[2]], len(docLenList))
	else:
		postingListForTerm = []
		termTuple = []
		
	p[0] = termTuple

def p_expression_quotes(p):
	'expression : QUOTE phrasal QUOTE'
	p[0] = retrieve.convertToTuple(p[2])

def p_phrasal_term(p):
	'phrasal : TERM'
	p[1] = p[1].lower()
	if indexMap.has_key(p[1]):
		offset = indexMap[p[1]][0]
		p[0] = retrieve.getPostingList(offset)
	else:
		p[0] = []
	
def p_phrasal_phrase(p):
	'phrasal : phrasal TERM'
	p[2] = p[2].lower()
	if indexMap.has_key(p[2]):
		offset = indexMap[p[2]][0]
		postingListForTerm = retrieve.getPostingList(offset)
	else:
		postingListForTerm = []
	p[0] = retrieve.mergePhrasalLists(p[1], postingListForTerm)

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"
    
# Build the parser
parser = yacc.yacc()

t1 = time.time()
indexMap = retrieve.readIndexMap()
print "Time to load indexMap = " +str(time.time() - t1)

t1 = time.time()
docLenList = readDocLenList()
print "Time to load docLenList = " +str(time.time() - t1)
    
while True:
   rankingMeasure = str(sys.argv[1]).lower()
   
   try:
       s = raw_input('Enter your query: ')
   except EOFError:
       break
   if not s: continue
   t1 = time.time()
   result = parser.parse(s)
   result.sort(key=lambda x: x[1], reverse=True)
   # sorted(result,key=lambda x: x[1])[::-1]
   for i in xrange(1,min(100,len(result))):
   	print result[i]
   # print result
   print "Time for query = " +str(time.time() - t1)
