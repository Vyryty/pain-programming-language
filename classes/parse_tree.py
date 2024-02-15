from classes.token import Token
from classes.expression import Expression
from classes.variable import Variable

class ParseTree:
    def __init__(self, tokens, errors: list[str]):
        self.tokens = tokens
        self.pointer = 0
        self.variables = {}
        self.matching: list[Token] = []
        self.errors = errors
        #self.root = self.parse()
        #print(self.root.evaluate())
        self.evaluate()
        for error in self.errors:
            print(error)

    def curr_token(self) -> Token:
        return None if self.pointer >= len(self.tokens) else self.tokens[self.pointer]

    def next_token(self) -> Token:
        self.pointer += 1
        return self.curr_token()
    
    def peek(self, amt) -> Token:
        self.pointer += amt
        val = self.curr_token()
        self.pointer -= amt
        return val

    def evaluate(self):
        execution = self.parse()
        if type(execution) == list:
            for i in execution:
                i.evaluate()
                #print(i.evaluate())
        else:
            return execution.evaluate()

    def parse(self, **kwargs) -> Expression:
        params = {
            "combine": True,
            "inParen": False,
            **kwargs
        }

        def submit_empty():
            return submit_exp("empty", "empty", [])

        def submit_invalid():
            return submit_exp("invalid", "invalid", [])

        def submit_exp (type, op, args):
            self.next_token()
            result = self.look_ahead(Expression(type, op, self.variables, args), **params)
            return result

        while self.curr_token() != None:
            token = self.curr_token()
            match token.type:
                case "blah":
                    word = token.string
                    if keywords.get(word) != None:
                        if type(keywords[word]) != Expression:
                            return keywords[word]
                        exp: Expression = keywords[word]
                        exp.vars = self.variables
                        match exp.type:
                            case "statement":
                                self.next_token()
                                if self.expect("(") >= 0:
                                    exp.args.append(submit_exp("parentheses", "parentheses", [self.parse(combine=False)]))
                                    if self.expect("{") >= 0:
                                        exp.args.append(submit_exp("contents", "contents", [self.parse(combine=False)]))
                                        return self.look_ahead(exp)
                                    else:
                                        return submit_exp("statement", exp.operation, exp.args[0])
                                else:
                                    return submit_exp("literal", "type", ["weapon"])
                            case "literal":
                                return self.look_ahead(exp)
                            case "binary":
                                self.errors.append(f"Thy left hand hath been lopped off at {token.location}!")

                    self.next_token()
                    if self.expect("(") >= 0:
                        print("Entering statment args!")
                        return submit_exp("statement", word, [self.parse(combine=False)])
                    return submit_exp("variable", "variable", [word])

                case "mathynum":
                    return submit_exp("literal", "mathynum", [token.value])
                
                case "num":
                    return submit_exp("literal", "num", [token.value])
                
                case "booboo":
                    return submit_exp("literal", "booboo", [token.value])
                
                case "quote":
                    value = ""
                    self.next_token()
                    while self.curr_token() != None and self.curr_token().type != "quote":
                        value += self.curr_token().string
                        self.next_token()
                    if self.curr_token() == None:
                        self.errors.append(f"Thou canst not defeat thine opponent lest thou finish thine battle cry at {token.location}!")
                    return submit_exp("literal", "blah", [value])
                
                case "open parenthesis":
                    self.matching.append(token)
                    self.next_token()
                    exp = Expression("parentheses", "parentheses", self.variables, self.parse(inParen=True))
                    close = self.expect(")", ",")
                    if close >= 0:
                        self.pointer += close
                        return submit_exp(exp.type, exp.operation, exp.args)
                    
                    self.errors.append(f"Thou hast a hole in thy container at {token.location}!")
                    return submit_invalid()

                case "close parenthesis":
                    if params["inParen"] and params["combine"]:
                        return submit_empty()
                    
                    self.errors.append(f"Thou mayest not finish what thou hast not started! Thou didst not open the container at {token.location}!")
                    return self.look_ahead(Expression("invalid", "invalid", self.variables, []))
                        
                case "open curly brace":
                    self.matching.append(token)
                    self.next_token()
                    exp = Expression("contents", "contents", self.variables, self.parse())
                    if self.expect("}") >= 0:
                        self.pointer += self.expect("}") + 1
                        return exp
                    
                    self.errors.append(f"Thou hast a hole in thy container at {token.location}!")
                    return self.look_ahead(Expression("invalid", "invalid", self.variables, []))
                
                case "close curly brace":
                    self.errors.append(f"Thou mayest not finish what thou hast not started! Thou didst not open the container at {token.location}!")
                    return self.look_ahead(Expression("invalid", "invalid", self.variables, []))
                
                case "open square bracket":
                    self.matching.append(token)
                    self.next_token()
                    exp = Expression("contents", "contents", self.variables, self.parse())
                    if self.expect("]") >= 0:
                        self.pointer += self.expect("]") + 1
                        return exp
                    
                    self.errors.append(f"Thou hast a hole in thy container at {token.location}!")
                    return self.look_ahead(Expression("invalid", "invalid", self.variables, []))

                case "comma":
                    self.next_token()
                    self.errors.append(f"Thou countest thine commas before they hatch at {token.location}!")

                case "whitespace":
                    self.next_token()
                case _:
                    self.errors.append(f"Canst thou not read? What thinkest thou of \"{self.curr_token().string}\" at {self.curr_token().location}?")
                    self.next_token()
                
        return None
    
    def expect(self, expected, ignore: str = "") -> bool:
        forward = 0
        while self.peek(forward) != None and ((self.peek(forward).type == "whitespace") or (self.peek(forward).string in ignore)):
            forward += 1
        if self.peek(forward) != None and self.peek(forward).string == expected:
            print(f"Found {expected}!")
            return forward
        print("Wanted:", expected, "Got:", self.peek(forward).string)
        print(forward)
        return -1

    def look_ahead(self, expression, **kwargs):
        if kwargs["combine"] and self.expect(",") >= 0:
            self.pointer += self.expect(",") + 1
            addition = self.parse(**kwargs)
            return [expression] + (addition if type(addition) == list else [addition])
        return [expression]

keywords = {
    "whilst": Expression("statement", "while", {}, []),
    "perchance": Expression("statement", "if", {}, []),
    "mightier": Expression("binary", "greater", {}, []),
    "respectable": Expression("binary", "greater equal", {}, []),
    "weaker": Expression("binary", "less", {}, []),
    "tolerable": Expression("binary", "less equal", {}, []),
    "worthy": Expression("binary", "equal", {}, []),
    "unworthy": Expression("binary", "equal", {}, []),
    "fool": Expression("unary", "not", {}, []),
    "counter": Expression("unary", "negate", {}, []),
    "yea": Expression("literal", "booboo", {}, [True]),
    "nay": Expression("literal", "booboo", {}, [False]),
    "naught": Expression("literal", "null", {}, [None])
}