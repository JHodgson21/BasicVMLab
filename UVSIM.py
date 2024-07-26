# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 14:37:02 2024

@author: Jakob, Jarek, Ben, Michael
"""
import sys
from FL import FileLoader
from IH import InstructionHandler4, InstructionHandler6

# Name of unittest file
TESTFILE = "UVSim Testing.py"

class UVSim:
    def __init__(self):
        self.memory = ['+000000'] * 249  # Initialize memory with +0000
        self.accumulator = 0
        self.instruction_counter = 0
        self.running = True
        self.file = FileLoader()

    def load_program(self, program):
        try:
            if (len(program) > 250):
                raise Exception("Programs must be no more than 250 lines long.")
            for i, instruction in enumerate(program):
                self.memory[i] = instruction
            self.instruction_counter = 0
            self.running = True
        except Exception as e:
            print(f"Unable to load program: {str(e)}")

    def fetch(self):
        inst = self.memory[self.instruction_counter]
        if (len(inst) == 5):
            instruction = InstructionHandler4(inst).parse()
        elif (len(inst) == 7):
            instruction = InstructionHandler6(inst).parse()
        self.instruction_counter += 1
        return instruction

    def decode_execute(self, instruction):
        
        operation = instruction[0]
        operand = instruction[1]
        if instruction[0] == '-':
            operation = -operation

        if operation == 10:  # READ
            pass  # READ is handled separately
        elif operation == 11:  # WRITE
            self.output(operand)
        elif operation == 20:  # LOAD
            self.accumulator = int(self.memory[operand])
        elif operation == 21:  # STORE
            self.memory[operand] = f'+{str(self.accumulator).zfill(4)}'
        elif operation == 30:  # ADD
            self.accumulator += int(self.memory[operand])
        elif operation == 31:  # SUBTRACT
            self.accumulator -= int(self.memory[operand])
        elif operation == 32:  # DIVIDE
            self.accumulator //= int(self.memory[operand])
        elif operation == 33:  # MULTIPLY
            self.accumulator *= int(self.memory[operand])
        elif operation == 40:  # BRANCH
            self.instruction_counter = operand
        elif operation == 41:  # BRANCHNEG
            if self.accumulator < 0:
                self.instruction_counter = operand
        elif operation == 42:  # BRANCHZERO
            if self.accumulator == 0:
                self.instruction_counter = operand
        elif operation == 43:  # HALT
            self.running = False
        self.validate(self.accumulator, instruction)

    def output(self, operand):
        print(int(self.memory[operand]))
        
    def validate(self, accumulator, instruction):
        if (len(instruction) == 5):
            if (accumulator > 9999 or accumulator < -9999):
                raise Exception("Resultant value larger than 9999 or smaller than -9999.")
        elif (len(instruction) == 7):
            if (accumulator > 999999 or accumulator < -999999):
                raise Exception("Resultant value is larger than 999999 or smaller than -999999.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python UVSIM.py <program_file.txt>")
        sys.exit(1)

    program_file = sys.argv[1]
    uvsim = UVSim()
    uvsim.file.program_name = program_file
    program = uvsim.file.get_program()

    uvsim.load_program(program)
    uvsim.run()
