from classes.token import Token
from classes.parse_tree import ParseTree

class Parser:
    def parse(tokens: list[Token], errors: list):
        tree = ParseTree(tokens, errors)