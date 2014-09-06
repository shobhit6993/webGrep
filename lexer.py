import ply.lex as lex

reserved = {
   'AND' : 'AND',
   'OR' : 'OR',
   'NOT' : 'NOT'
}

# List of token names.
tokens = ['QUOTE', 'LPAREN', 'RPAREN', 'TERM'] + list(reserved.values())

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_QUOTE = r'"'

# Match anything but whitespace
def t_TERM(t):
    r'[^\( \) "  \t\n\r\f]+'
    t.type = reserved.get(t.value, 'TERM')    # Check for reserved words
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\n\r\f'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
    
# Build the lexer
lexer = lex.lex()

