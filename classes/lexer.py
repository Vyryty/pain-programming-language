from classes.token import Token
from classes.location import Location

class Lexer:
    def lex(string: str, line_number: int, file: str):
        tokens = []
        errors = []

        index = 0
        while index < len(string):
            # Add string tokens
            if string[index].isalpha():
                start_index = index + 1
                word = string[index]
                index += 1
                while index < len(string) and string[index].isalnum():
                    word += string[index]
                    index += 1
                
                tokens.append(Token(word,
                                    word,
                                    "blah",
                                    Location(line_number, start_index, len(word), file)))
            
            # Add floats and ints
            elif string[index].isdigit() or string[index] == ".":
                start_index = index + 1
                decimal = string[index] == "."
                word = string[index]
                index += 1
                while index < len(string) and string[index].isdigit():
                    word += string[index]
                    index += 1
                
                if decimal and len(word) <= 1:
                    tokens.append(Token.invalid_token(".", Location(line_number, index + 1, 1, file)))
                    continue
                
                if index < len(string) and string[index] == "." and not decimal:
                    decimal = True
                    word += string[index]
                    index += 1
                    while index < len(string) and string[index].isdigit():
                        word += string[index]
                        index += 1
                
                if not decimal or len(word) > 1:
                    tokens.append(Token(word,
                                        float(word) if decimal else int(word),
                                        "mathynum" if decimal else "num",
                                        Location(line_number, start_index, len(word), file)))
                else:
                    index -= 1
            
            elif string[index].isspace():
                start_index = index + 1
                word = ""
                while index < len(string) and string[index].isspace():
                    word += string[index]
                    index += 1
                
                tokens.append(Token(word,
                                    "<space>",
                                    "whitespace",
                                    Location(line_number, start_index, len(word), file)))

            else:   
                match (string[index]):
                    case "$":
                        break
                    case ".":
                        tokens.append(Token(string[index],
                                            string[index],
                                            "dot",
                                            Location(line_number, index + 1, 1, file)))
                        index += 1
                    case "\"":
                        tokens.append(Token(string[index],
                                            string[index],
                                            "quote",
                                            Location(line_number, index + 1, 1, file)))
                        index += 1
                    case "=":
                        tokens.append(Token(string[index],
                                            string[index],
                                            "equals",
                                            Location(line_number, index + 1, 1, file)))
                        index += 1
                    case "+":
                        tokens.append(Token(string[index],
                                            string[index],
                                            "plus",
                                            Location(line_number, index + 1, 1, file)))
                        index += 1
                    case "-":
                        tokens.append(Token(string[index],
                                            string[index],
                                            "dash",
                                            Location(line_number, index + 1, 1, file)))
                        index += 1
                    case "*":
                        tokens.append(Token(string[index],
                                            string[index],
                                            "star",
                                            Location(line_number, index + 1, 1, file)))
                        index += 1
                    case "/":
                        tokens.append(Token(string[index],
                                            string[index],
                                            "slash",
                                            Location(line_number, index + 1, 1, file)))
                        index += 1
                    case "(":
                        tokens.append(Token(string[index],
                                            string[index],
                                            "open parenthesis",
                                            Location(line_number, index + 1, 1, file)))
                        index += 1
                    case ")":
                        tokens.append(Token(string[index],
                                            string[index],
                                            "close parenthesis",
                                            Location(line_number, index + 1, 1, file)))
                        index += 1
                    case "{":
                        tokens.append(Token(string[index],
                                            string[index],
                                            "open curly brace",
                                            Location(line_number, index + 1, 1, file)))
                        index += 1
                    case "}":
                        tokens.append(Token(string[index],
                                            string[index],
                                            "close curly brace",
                                            Location(line_number, index + 1, 1, file)))
                        index += 1
                    # case "[":
                    #     tokens.append(Token(string[index],
                    #                         string[index],
                    #                         "open square bracket",
                    #                         Location(line_number, index + 1, 1, file)))
                    #     index += 1
                    # case "]":
                    #     tokens.append(Token(string[index],
                    #                         string[index],
                    #                         "close square bracket",
                    #                         Location(line_number, index + 1, 1, file)))
                    case ",":
                        tokens.append(Token(string[index],
                                            string[index],
                                            "comma",
                                            Location(line_number, index + 1, 1, file)))
                        index += 1
                    case _:
                        tokens.append(Token.invalid_token(string[index], Location(line_number, index + 1, 1, file)))
                        index += 1
        
        return tokens, errors