class InstructionHandler:
    def __init__(self, instruction):
        self.instruction = instruction
    
    def parse(self):
        halfpoint = (len(self.instruction)//2) + 1
        length = (halfpoint - 1) * 2
        sign = self.instruction[0]
        opcode = int(self.instruction[1:halfpoint])
        operand = int(self.instruction[(halfpoint):(len(self.instruction))])
        instruction_info = [opcode, operand, length, sign]
        return instruction_info




class InputHandler:
    def __init__(self, input, length):
        self.input = input
        self.length = length
        
    def validate(self):
        if (self.length == 4):
            max = 9999
        elif (self.length == 6):
            max = 9999
            
        if (self.input > max or self.input < -max):
            raise Exception(f"Value larger than {max} or smaller than -{max}.")
        else:
            return True
