# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 20:31:40 2024

@authors: Jakob, Ben, Michael, Jarek
"""

import unittest
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

    # Test cases for Use Case #5: Addition Operation

    def test_successful_addition(self):
        self.uvsim.memory[5] = 20
        self.uvsim.accumulator = 15
        self.add(5)
        self.assertEqual(self.uvsim.accumulator, 35)

    def test_addition_with_overflow(self):
        self.uvsim.memory[5] = 9999
        self.uvsim.accumulator = 9999
        with self.assertRaises(OverflowError):
            self.add(5)

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
    
    # Test cases for Use Case #7: Multiplication Operation
    def test_successful_multiplication(self):
        self.uvsim.memory[5] = 3
        self.uvsim.accumulator = 2
        self.multiply(5)
        self.assertEqual(self.uvsim.accumulator, 6)
    
    def test_multiplication_resulting_in_negative(self):
        self.uvsim.memory[5] = 2
        self.uvsim.accumulator = -6
        self.multiply(5)
        self.assertEqual(self.uvsim.accumulator, -12)
    
    # Test cases for Use Case #8: Division Operation
    def test_successful_division(self):
        self.uvsim.memory[5] = 5
        self.uvsim.accumulator = 20
        self.divide(5)
        self.assertEqual(self.uvsim.accumulator, 4)
    
    def test_division_resulting_in_negative(self):
        self.uvsim.memory[5] = -3
        self.uvsim.accumulator = 60
        self.divide(5)
        self.assertEqual(self.uvsim.accumulator, -20)

    # Auxiliary methods for UVSim operations used in tests
    def add(self, memory_location):
        add_operation = '+3000'
        add_operation = add_operation[:-1] + str(memory_location)
        self.uvsim.decode_execute(add_operation)

    def subtract(self, memory_location):
        sub_operation = '+3100'
        sub_operation = sub_operation[:-1] + str(memory_location)
        self.uvsim.decode_execute(sub_operation)
    
    def multiply(self, memory_location):
        self.uvsim.decode_execute(3300 + memory_location)
    
    def divide(self, memory_location):
        self.uvsim.decode_execute(3200 + memory_location)

    def read(self, memory_location):
        read_operation = '+1000'
        read_operation = read_operation[:-1] + str(memory_location)
        self.uvsim.decode_execute(read_operation)

    def load(self, memory_location):
        load_operation = '+2000'
        load_operation = load_operation[:-1] + str(memory_location)
        self.uvsim.decode_execute(load_operation)


if __name__ == "__main__":
    unittest.main()
