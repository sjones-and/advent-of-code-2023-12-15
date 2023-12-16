#!/usr/bin/env python3

import os
from time import perf_counter_ns

def answer(input_file):
    start = perf_counter_ns()
    answer = 0
    with open(input_file, 'r') as input:
        value = 0
        while next_char := input.read(1):
            if next_char == ',':
                answer += value
                value = 0
            else:
                value = ((value + ord(next_char)) * 17) % 256

    end = perf_counter_ns()

    print(f'The answer is: {answer}')
    print(f'{((end-start)/1000000):.2f} milliseconds')

input_file = os.path.join(os.path.dirname(__file__), 'input')
answer(input_file)
