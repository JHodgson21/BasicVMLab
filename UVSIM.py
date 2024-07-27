# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 14:37:02 2024

@author: Jakob, Jarek, Ben, Michael
"""
import sys
from FL import FileLoader
from IH import InstructionHandler, InputHandler

# Name of unittest file
TESTFILE = "UVSim Testing.py"

class UVSim:
    def __init__(self):
        self.memory = ['+000000'] * 250  # Initialize memory with +0000
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
        info = InstructionHandler(inst).parse()
        self.instruction_counter += 1
        return info

    def decode_execute(self, instruction):
        opcode = instruction[0]
        operand = instruction[1] 
        length = instruction[2]

        if opcode == 10:  # READ
            pass  # READ is handled separately
        elif opcode == 11:  # WRITE
            self.output(operand)
        elif opcode == 20:  # LOAD
            self.accumulator = int(self.memory[operand])
        elif opcode == 21:  # STORE
            if length == 4:
                self.memory[operand] = f'+{str(self.accumulator).zfill(4)}'
            elif length == 6:
                self.memory[operand] = f'+{str(self.accumulator).zfill(6)}'
        elif opcode == 30:  # ADD
            self.accumulator += int(self.memory[operand])
        elif opcode == 31:  # SUBTRACT
            self.accumulator -= int(self.memory[operand])
        elif opcode == 32:  # DIVIDE
            self.accumulator //= int(self.memory[operand])
        elif opcode == 33:  # MULTIPLY
            self.accumulator *= int(self.memory[operand])
        elif opcode == 40:  # BRANCH
            self.instruction_counter = operand
        elif opcode == 41:  # BRANCHNEG
            if self.accumulator < 0:
                self.instruction_counter = operand
        elif opcode == 42:  # BRANCHZERO
            if self.accumulator == 0:
                self.instruction_counter = operand
        elif opcode == 43:  # HALT
            self.running = False
        InputHandler(self.accumulator, length).validate()

    def output(self, operand):
        print(int(self.memory[operand]))

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
