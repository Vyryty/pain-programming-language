class Expression:
    def __init__(self, type, operation, args):
        self.type = type
        self.operation = operation
        self.args = args

    def evaluate(self):
        match self.type:
            case "literal":
                return self.args[0]
            case "statement":
                pass
            case "container":
                # use args[0] as entry character
                # evaluate expression
                # demand args[-1] matches args[0]
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
                    
    def __add__(self, x):
        return self.evaluate() + x.evaluate()
    
    def __sub__(self, x):
        return self.evaluate() - x.evaluate()
    
    def __mul__(self, x):
        return self.evaluate() * x.evaluate()
    
    def __truediv__(self, x):
        return self.evaluate() / x.evaluate()