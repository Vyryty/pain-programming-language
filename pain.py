from classes.lexer import Lexer
from classes.parse_tree import ParseTree
import tkinter.filedialog as fd
from os import getcwd

tokens = []
errors = []
file_name = fd.askopenfilename(initialdir=getcwd(), title="Open Pain File", filetypes=[("*.pain", "Pain File")])

with open(file_name, "r") as file:
    line_number = 1
    for line in file.readlines():
        new_tokens, new_errors = Lexer.lex(line, line_number, file_name)
        tokens += new_tokens
        errors += new_errors
        line_number += 1

# for token in tokens:
#     print(str(token))

parser = ParseTree(tokens, errors)
parser.print_tree()
parser.evaluate()
parser.print_errors()