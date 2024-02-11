class Location:
    def __init__(self, line_number, column, length, file_name):
        self.line_number = line_number
        self.column = column
        self.length = length
        self.file_name = file_name

    def __str__(self):
        return f"({self.file_name}, {self.line_number}:{self.column}:{self.length})"