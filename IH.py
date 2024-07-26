class InstructionHandler4:
    def __init__(self, instruction):
        self.operation = abs(int(instruction[1:3]))
        self.operand = int(instruction[3:5])

    def parse(self):
        return [self.operation, self.operand]

class InstructionHandler6:
    def __init__(self, instruction):
        self.operation = abs(int(instruction[1:4]))
        self.operand = int(instruction[5:7])
        
    def parse(self):
        return [self.operation, self.operand]
