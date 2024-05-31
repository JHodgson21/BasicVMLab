# -*- coding: utf-8 -*-
"""
Created on Wed May 22 17:37:33 2024

@author: Jakob
"""

class UVSim:
    def __init__(self):
        self.memory = [0] * 100  # 100 memory initialized to zero
        self.accumulator = 0  # Accumulator register
        self.instruction_counter = 0  #Instructions counter
        self.running = True  # Simulator running

    def load_program(self, program):
        """ Load the program into the memory starting at location 0 """
        for i, instruction in enumerate(program):
            self.memory[i] = instruction

    def fetch(self):
        """ Fetch the next instruction """
        instruction = self.memory[self.instruction_counter]
        self.instruction_counter += 1
        return instruction

    def decode_execute(self, instruction):
        """ Decode and execute the instruction """
        opcode = instruction // 100  # First two digits
        operand = instruction % 100  # Last two digits

        if opcode == 10:  # READ
            value = int(input("Enter an integer: "))
            self.memory[operand] = value
        elif opcode == 11:  # WRITE
            print(self.memory[operand])
        elif opcode == 20:  # LOAD
            self.accumulator = self.memory[operand]
        elif opcode == 21:  # STORE
            self.memory[operand] = self.accumulator
        elif opcode == 30:  # ADD
            self.accumulator += self.memory[operand]
        elif opcode == 31:  # SUBTRACT
            self.accumulator -= self.memory[operand]
        elif opcode == 32:  # DIVIDE
            if self.memory[operand] == 0:
                raise ZeroDivisionError("Attempted division by zero")
            self.accumulator //= self.memory[operand]
        elif opcode == 33:  # MULTIPLY
            self.accumulator *= self.memory[operand]
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
        else:
            raise ValueError(f"Unknown opcode {opcode}")

    def run(self):
        """ Run the simulation """
        while self.running:
            instruction = self.fetch()
            self.decode_execute(instruction)

# Example Run (we will need to use the file the prof gives us).
program = [
    1007,  # READ to memory location 07
    1008,  # READ to memory location 08
    2007,  # LOAD from memory location 07
    3008,  # ADD from memory location 08
    2109,  # STORE to memory location 09
    1109,  # WRITE from memory location 09
    4300   # HALT
]

# Creating a uvsim instance
uvsim = UVSim()

# Loading the program in memory
uvsim.load_program(program)

#Run it!
uvsim.run()
