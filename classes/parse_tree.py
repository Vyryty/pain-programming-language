from classes.token import Token
from classes.expression import Expression
from classes.variable import Variable

class ParseTree:
    def __init__(self, tokens, errors: list[str]):
        self.tokens = tokens
        self.pointer = 0
        self.variables = {}
        self.errors = errors
        self.root = Expression("execution", "execute", self.variables, [self.parse()])

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
        return self.root.evaluate()
    
    def print_errors(self):
        for error in self.errors:
            print(error)
    
    def print_tree(self) -> str:
        def print_exp(exp, prefix = "", hasNextSibling=False):
            add_pref = "├── " if hasNextSibling else "└── "
            if type(exp) == Expression:
                print(f"{prefix + add_pref}{exp.operation}")
                children_pref = "│   " if hasNextSibling else "    "
                for i, arg in enumerate(exp.args):
                    print_exp(arg, prefix + children_pref, i < len(exp.args) - 1)
            else:
                print(f"{prefix + add_pref}{exp}")
        print_exp(self.root)

    def parse(self, **kwargs) -> Expression:
        default_params = {
            "combine": True,
            "inParen": False,
            "acceptEmpty": False,
        }
        params = {
            **default_params,
            **kwargs,
        }

        def submit_empty():
            return submit_exp("empty", "empty", [])

        def submit_invalid():
            return submit_exp("invalid", "invalid", [])

        def submit_parse_exp(type, op, **kwargs):
            self.next_token()
            return self.look_ahead(Expression(type, op, self.variables, [self.parse(**kwargs)]), **params)

        def submit_exp (type, op, args):
            self.next_token()
            return self.look_ahead(Expression(type, op, self.variables, args), **params)

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
                        # Update to use submit_parse_exp
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

                    if self.expect("(") >= 0:
                        return submit_parse_exp("statement", word, combine=False, acceptEmpty=True)
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
                
                case "comma":
                    self.errors.append(f"Thou countest thine commas before they hatch at {token.location}!")
                    return submit_invalid()

                case "whitespace":
                    self.next_token()
                
                case _:
                    container = self.open_container(token, submit_parse_exp, submit_invalid)
                    if container != None:
                        return container
                    container = self.close_container(token, submit_empty, submit_invalid, **params)
                    if container != None:
                        return container

                    self.errors.append(f"Canst thou not read? What thinkest thou of \"{self.curr_token().string}\" at {self.curr_token().location}?")
                    return submit_invalid()
                
        return None
    
    def open_container(self, token, submit_parse_exp, submit_invalid):
        exp = None
        match = ""
        match token.type:
            case "open parenthesis":
                exp = submit_parse_exp("parentheses", "parentheses", inParen=True)
                match = ")"
            case "open curly brace":
                exp = submit_parse_exp("contents", "contents", inParen=True)
                match = "}"
            case _:
                return None

        #print(exp[-1].args[-1].type)
        if exp != None and len(exp) > 0 and (exp[-1] == None or (len(exp[-1].args) > 0 and (exp[-1].args[-1] == None or exp[-1].args[-1].type == "empty"))):
            print("Empty!")
            self.pointer -= 1

        close = self.expect(match, ",", forward=False)
        if close >= 0:
            self.pointer += close + 1
            return exp
        
        self.errors.append(f"Thou hast a hole in thy container at {token.location}!")
        return submit_invalid()
    
    def close_container(self, token, submit_empty, submit_invalid, **params):
        match token.type:
            case "close parenthesis":
                pass
            case "close curly brace":
                pass
            case _:
                return None

        if params["inParen"] and params["combine"]:
            return submit_empty()
        
        self.errors.append(f"Thou mayest not finish what thou hast not started! Thou didst not open the container at {token.location}!")
        return submit_invalid()

    def expect(self, expected, ignore: str = "", forward = True) -> int:
        forward = 1 if forward else 0
        while self.peek(forward) != None and ((self.peek(forward).type == "whitespace") or (self.peek(forward).string in ignore)):
            forward += 1
        if self.peek(forward) != None and self.peek(forward).string == expected:
            #print(f"Found {expected} At:", self.peek(forward).location.column)
            return forward
        #print("Wanted:", expected, "At:", self.peek(forward).location.column, "( Forward:", forward, ") Got:", self.peek(forward).string)
        return -1

    def expect_one(self, expected: str, ignore: str = "", forward = True) -> tuple[str, int]:
        for i in expected:
            index = self.expect(i, ignore, forward)
            if index >= 0:
                return i, index
        return None, -1

    def look_ahead(self, expression, **kwargs):
        comma = self.expect(",", forward=False)
        if kwargs["combine"] and comma >= 0:
            self.pointer += comma + 1
            addition = self.parse(**kwargs)
            return [expression] + (addition if type(addition) == list else [addition])
        
        op = self.expect_one("+-*/", forward=False)
        if kwargs["combine"] and op[1] >= 0:
            print("Found", op[0])
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