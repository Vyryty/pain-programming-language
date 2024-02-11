from classes.lexer import Lexer
from classes.parser import Parser
import tkinter.filedialog as fd
from os import getcwd

tokens = []
file_name = fd.askopenfilename(initialdir=getcwd(), title="Open Pain File", filetypes=[("*.pain", "Pain File")])

with open(file_name, "r") as file:
    tokens = []
    errors = []
    line_number = 1
    for line in file.readlines():
        new_tokens, new_errors = Lexer.lex(line, line_number, file_name)
        tokens += new_tokens
        errors += new_errors
        line_number += 1

for token in tokens:
    print(str(token))

#Parser.parse(tokens, errors)