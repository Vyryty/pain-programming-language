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
                start_index = index
                word = string[index]
                index += 1
                while index < len(string) and string[index].isalnum():
                    word += string[index]
                    index += 1
                
                tokens.append(Token(word,
                                    word,
                                    "word",
                                    Location(line_number, start_index, len(word), file)))
            
            # Add floats and ints
            elif string[index].isdigit() or string[index] == ".":
                start_index = index
                decimal = string[index] == "."
                word = string[index]
                index += 1
                while index < len(string) and string[index].isdigit():
                    word += string[index]
                    index += 1
                
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
                                        "float" if decimal else "int",
                                        Location(line_number, start_index, len(word), file)))
                else:
                    index -= 1
            
            elif string[index].isspace():
                start_index = index
                word = ""
                while index < len(string) and string[index].isspace():
                    word += string[index]
                    index += 1
                
                tokens.append(Token("<space>",
                                    "<space>",
                                    "whitespace",
                                    Location(line_number, start_index, len(word), file)))

            else:   
                match (string[index]):
                    case "~":
                        tokens.append(Token(string[index],
                                            string[index],
                                            "tilde",
                                            Location(line_number, index, 1, file)))
                        break
                    case ".":
                        tokens.append(Token(string[index],
                                            string[index],
                                            "dot",
                                            Location(line_number, index, 1, file)))
                        index += 1
                    case _:
                        tokens.append(Token.invalid_token(string[index], Location(line_number, index, 1, file)))
                        index += 1
        
        return tokens, errors