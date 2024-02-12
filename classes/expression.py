class Expression:
    def __init__(self, type: str, operation: str, vars: dict, args: list):
        self.type = type
        self.operation = operation
        self.vars = vars
        self.args = args

    def evaluate(self):
        self.args = self.unpack_expression_chain(self.args)

        match self.type:
            case "literal":
                return self.args[0]
            case "statement":
                return execute(self.operation, self.args)
            case "parentheses":
                result = []
                for arg in self.args:
                    result.append(arg)
                return result
            case "contents":
                pass
            case "indexer":
                pass
            case "variable":
                pass 
            case "expression":
                match self.operation:
                    case "+":
                        total = 0
                        for arg in self.args:
                            total += arg
                        return total
                    case "-":
                        total = 0
                        for arg in self.args:
                            total -= arg
                        return total
                    case "*":
                        total = 1
                        for arg in self.args:
                            total *= arg
                        return total
                    case "/":
                        total = self.args[0] ** 2
                        for arg in self.args:
                            total /= arg
                        return total
            case "invalid":
                pass
            case _:
                raise "Invalid expression type!"
            
    def unpack_expression_chain(self, chain):
        chain = unpack_list(chain)
        if type(chain) == list:
            for i in range(len(chain)):
                chain[i] = self.unpack_expression_chain(chain[i])
        elif type(chain) == Expression:
            return chain.evaluate()
        return unpack_list(chain)
                    
def execute(function, args):
    match function:
        case "cry":
            if type(args) == list and len(args) > 0:
                return print(*[str(arg) for arg in args])
            elif type(args) == list:
                return print()
            return print(args)
        case "kind":
            if type(args) == bool:
                return "booboo"
            elif type(args) == int:
                return "num"
            elif type(args) == float:
                return "mathynum"
            elif type(args) == str:
                return "blah"
            else:
                raise "Invalid type!"
            
def unpack_list(packed_list):
    if type(packed_list) == list:
        while len(packed_list) == 1 and type(packed_list[0]) == list:
            packed_list = packed_list[0]
        for i in packed_list:
            unpack_list(i)
    return packed_list