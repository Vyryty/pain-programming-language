"""Class to represent a syntax token"""
class Token:
    def __init__(self, string, value, type, location):
        self.string = string
        self.value = value
        self.type = type
        self.location = location

    def invalid_token(string: str, location):
        return Token(string, string, "invalid", location)
    
    def __str__(self):
        return f"<{self.type} token: \"{'<space>' if self.string.isspace() else self.string}\" at {str(self.location)}>"