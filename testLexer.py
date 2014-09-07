import lexer

# Test it out
data = '"hihfih	ih	ihi" (+64561561) AND pki	pokpk OR fqwKJFMOkmokm NOT 291y9889' 

# Give the lexer some input
lexer.lexer.input(data)

# Tokenize
while True:
    tok = lexer.lexer.token()
    if not tok: break      # No more input
    print tok
