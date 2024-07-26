class InstructionHandler4:
    def __init__(self, instruction):
        self.instruction = instruction[1:5]
        self.operation = abs(int(instruction[1:3]))
        self.operand = int(instruction[3:5])

    def parse(self):
<<<<<<< Updated upstream
        if (self.operand > 249 or self.operand < 0):
            raise Exception("Invalid Memory Address")
        else:
            return [self.operation, self.operand]
=======
        return [self.operation, self.operand, self.instruction]
>>>>>>> Stashed changes

class InstructionHandler6:
    def __init__(self, instruction):
        self.instruction = instruction[1:7]
        self.operation = abs(int(instruction[1:4]))
        self.operand = int(instruction[5:])
        
    def parse(self):
<<<<<<< Updated upstream
        if(self.operand > 249 or self.operand < 0):
            raise Exception("Invalid Memory Address")
        else: return [self.operation, self.operand]
=======
        return [self.operation, self.operand, self.instruction]
>>>>>>> Stashed changes
