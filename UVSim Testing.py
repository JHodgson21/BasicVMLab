# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 20:31:40 2024

@authors: Jakob, Ben, Michael, Jarek
"""

import unittest
import unittest.mock
import io
from UVSIM import UVSim

class TestUVSim(unittest.TestCase):

    def setUp(self):
        self.uvsim = UVSim()

    # Test cases for Use Case #1: Load Program

    def test_successful_program_load(self):
        program = ['+1007', '+1008', '+2007', '+3108', '+2109', '+1109', '+4300']
        self.uvsim.load_program(program)
        self.assertEqual(self.uvsim.instructions[:len(program)], program)

    def test_invalid_instruction(self):
        program = ['+1007', '+9999', '+2007', '+3108', '+2109', '+1109', '+4300']
        with self.assertRaises(ValueError):
            self.uvsim.load_program(program)
            self.uvsim.run()  # Make sure that the invalid instruction is caught during run
            
    # Test case for Use Case #2: I/O Read
    
    def test_successful_read(self):
        self.uvsim.memory[0] = 0
        self.read(0)
        self.assertEqual(self.uvsim.memory[0], 1) # ASSUMES USER ENTER 1 after ...Enter an integer: 

    # Test cases for Use Case #4 Load Operation
    
    def test_successful_load(self):
        self.uvsim.memory[0] = 12
        self.load(0)
        self.assertEqual(self.uvsim.accumulator, 12)
    
    def test_successful_load(self):
        self.uvsim.memory[0] = 15
        self.load(0)
        self.assertEqual(self.uvsim.accumulator, 15)

    #Test Cases for Use Case #3: Write Operation

    def test_successful_write(self):
        program = [
            '+1108', # READ 08 TO SCREEN
            '+4300'  # TERMINATE
        ]
        self.uvsim.load_program(program)
        self.uvsim.memory[8] = 5
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.uvsim.run()
            self.assertEqual(mock_stdout.getvalue(), '5\n')
    
    def test_multiple_writes(self):
        program = [
            '+1108', # READ 08 TO SCREEN
            '+1109', # READ 09 TO SCREEN
            '+4300'  # TERMINATE
        ]
        self.uvsim.load_program(program)
        self.uvsim.memory[8], self.uvsim.memory[9] = 14, 72
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.uvsim.run()
            self.assertEqual(mock_stdout.getvalue(), '14\n72\n')

    # Test cases for Use Case #5: Addition Operation

    def test_successful_addition(self):
        self.uvsim.memory[5] = 20
        self.uvsim.accumulator = 15
        self.add(5)
        self.assertEqual(self.uvsim.accumulator, 35)

    def test_addition_with_zero(self):
        self.uvsim.memory[5] = 0
        self.uvsim.accumulator = 15
        self.add(5)
        self.assertEqual(self.uvsim.accumulator, 15) #make sure adding zero doesn't change the accumulator. 

    # Test cases for Use Case #6: Subtraction Operation

    def test_successful_subtraction(self):
        self.uvsim.memory[5] = 10
        self.uvsim.accumulator = 25
        self.subtract(5)
        self.assertEqual(self.uvsim.accumulator, 15)

    def test_subtraction_resulting_in_negative(self):
        self.uvsim.memory[5] = 30
        self.uvsim.accumulator = 10
        self.subtract(5)
        self.assertEqual(self.uvsim.accumulator, -20)

    def test_subtraction_with_zero(self):
        self.uvsim.memory[5] = 0
        self.uvsim.accumulator = 15
        self.subtract(5)
        self.assertEqual(self.uvsim.accumulator, 15) #make sure subtracting zero doesn't change accumulator. 
    
    # Test cases for Use Case #7: Multiplication Operation

    def test_successful_multiplication(self):
        self.uvsim.memory = [0] * 11
        self.uvsim.memory[8] = 4
        self.uvsim.memory[9] = 5
        self.multiply()
        self.assertEqual(self.uvsim.memory[10], 20)
    
    def test_negative_multiplication(self):
        self.uvsim.memory = [0] * 11
        self.uvsim.memory[8] = -4
        self.uvsim.memory[9] = 5
        self.multiply()
        self.assertEqual(self.uvsim.memory[10], -20)

    # Test cases for Use Case #8: Division Operation

    def test_successful_division(self):
        self.uvsim.memory = [0] * 11
        self.uvsim.memory[8] = 20
        self.uvsim.memory[9] = 4
        self.divide()
        self.assertEqual(self.uvsim.memory[10], 5)
    
    def test_divide_by_zero(self):
        self.uvsim.memory = [0] * 11
        self.uvsim.memory[8] = 20
        with self.assertRaises(ZeroDivisionError):
            self.divide()

    # Test cases for Use Case #9: BRANCH Operation

    def test_successful_branch(self):
        self.uvsim.instructions = [
            "+2008", # LOAD 08 TO ACC
            "+4005", # BRANCH TO 05 (NOTE: The program should skip to location 05 and NOT run operations 02 through 04)
            "+3309", # MULTIPLY 09 TO ACC
            "+2111", # STORE ACC TO 11
            "+4300", # TERMINATE
            "+3310", # MULTIPLY 10 TO ACC
            "+2111", # STORE ACC TO 11
            "+4300" # TERMINATE
        ]
        self.uvsim.memory = [0] * 12
        self.uvsim.memory[8] = 5
        self.uvsim.memory[9] = -30
        self.uvsim.memory[10] = 5
        self.uvsim.run()
        self.assertEqual(self.uvsim.memory[11], 25)
    
    def test_branch_to_halt(self):
        self.uvsim.instructions = [
            "+2008", # LOAD 08 TO ACC 
            "+2111", # STORE ACC TO 11
            "+4005", # BRANCH TO 05 (NOTE: The program should skip to 05 and read the instruction there, not pass over it and proceed.)
            "+2009", # LOAD 09 TO ACC
            "+2111", # STORE ACC TO 11
            "+4300", # TERMINATE
            "+2010", # LOAD 10 TO ACC
            "+2111", # STORE ACC TO 11
            "+4300", # TERMINATE
        ]
        self.uvsim.memory = [0] * 12
        self.uvsim.memory[8], self.uvsim.memory[9], self.uvsim.memory[10] = 1, 2, 3
        self.uvsim.run()
        self.assertEqual(self.uvsim.memory[11], 1)
    
    # Test cases for Use Case #10: BRANCHNEG Operation
    
    def test_successful_branchneg(self):
        self.uvsim.instructions = [
            "+2008", # LOAD 08 TO ACC
            "+2111", # STORE ACC TO 11
            "+4105", # BRANCH TO 05 IF ACC IS NEGATIVE
            "+2009", # LOAD 09 TO ACC
            "+2111", # STORE ACC TO 11
            "+4300", # TERMINATE
            "+2010", # LOAD 10 TO ACC
            "+2111", # STORE ACC TO 11
            "+4300", # TERMINATE
        ]
        self.uvsim.memory = [0] * 12
        self.uvsim.memory[8], self.uvsim.memory[9], self.uvsim.memory[10] = 1, -2, 3
        self.uvsim.run()
        self.assertEqual(self.uvsim.memory[11], -2)

    def test_branchneg_loop(self):
        # Runs a loop 6 times to accomplish the expression: 4 * 2^6
        self.uvsim.instructions = [
            "+2008", # LOAD 08 TO ACC
            "+4108", # BRANCH TO 08 IF ACC IS NEGATIVE
            "+3109", # SUBTRACT 09 FROM ACC (09 IS 1)
            "+2108", # STORE ACC TO 08
            "+2010", # LOAD 10 TO ACC
            "+3311", # MULTIPLY 11 TO ACC
            "+2110", # STORE ACC TO 10
            "+4000", # BRANCH TO 00
            "+2010", # LOAD 10 TO ACC
            "+2112", # STORE ACC TO 12
            "+4300", # TERMINATE
        ]
        self.uvsim.memory = [0] * 13
        self.uvsim.memory[8] = 5 # Iterator
        self.uvsim.memory[9] = 1 # Incrementor
        self.uvsim.memory[10] = 4 # Number to be multiplied
        self.uvsim.memory[11] = 2 # Multiplier
        self.uvsim.run()
        self.assertEqual(self.uvsim.memory[12], 256)

    # Auxiliary methods for UVSim operations used in tests
    def add(self, memory_location):
        add_operation = '+3000'
        add_operation = add_operation[:-1] + str(memory_location)
        self.uvsim.decode_execute(add_operation)

    def subtract(self, memory_location):
        sub_operation = '+3100'
        sub_operation = sub_operation[:-1] + str(memory_location)
        self.uvsim.decode_execute(sub_operation)
    
    def multiply(self):
        self.uvsim.instructions = [
            "+2008", # LOAD 08 TO ACC
            "+3309", # MULTIPLY 09 TO ACC
            "+2110", # STORE TO 10
            "+1108", # WRITE 10 TO SCREEN
            "+4300"  # TERMINATE
        ]
        self.uvsim.run()

    def divide(self):
        self.uvsim.instructions = [
            "+2008", # LOAD 08 TO ACC
            "+3209", # DIVIDE ACC BY 09
            "+2110", # STORE TO 10
            "+1108", # WRITE 10 TO SCREEN
            "+4300" #TERMINATE
        ]
        self.uvsim.run()
        
    def read(self, memory_location):
        read_operation = '+1000'
        read_operation = read_operation[:-1] + str(memory_location)
        self.uvsim.decode_execute(read_operation)

    def load(self, memory_location):
        load_operation = '+2000'
        load_operation = load_operation[:-1] + str(memory_location)
        self.uvsim.decode_execute(load_operation)


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
