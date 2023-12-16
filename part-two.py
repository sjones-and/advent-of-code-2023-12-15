#!/usr/bin/env python3

import os
from functools import reduce
from time import perf_counter_ns

class Box:
    def __init__(self, index, box_collection):
        self.index = index
        self.next_index = 0
        self.mapping = {}
        self.lenses = {}
        self.box_collection = box_collection

    def store(self, lens):
        if lens.label in self.mapping:
            self.lenses[self.mapping[lens.label]] = lens
        else:
            self.lenses[self.next_index] = lens
            self.mapping[lens.label] = self.next_index
            self.next_index += 1
            self.box_collection.register(lens.label, self.index)

    def delete(self, lens):
        if lens.label in self.mapping:
            self.lenses.pop(self.mapping[lens.label])
            self.mapping.pop(lens.label)
            self.box_collection.deregister(lens.label)

    def get_score(self):
        lens_scores = 0
        lens_keys = sorted(self.lenses.keys())
        for ix in range(len(lens_keys)):
            lens_scores += ((ix + 1) * self.lenses[lens_keys[ix]].focal_length)
        return lens_scores * (self.index + 1)

    def add_score(score, box):
        return score + box.get_score()

class BoxCollection:
    def __init__(self):
        self.boxes = {
            ix: Box(ix, self)
            for ix in range(256)
        }
        self.mapping = {}
    
    def register(self, label, box_number):
        self.mapping[label] = box_number
    
    def deregister(self, label):
        if label in self.mapping:
            self.mapping.pop(label)

    def process(self, lens):
        box = None
        if lens.label in self.mapping:
            box = self.boxes[self.mapping[lens.label]]
        else:
            box = self.boxes[lens.hash]
        
        if lens.delete:
            box.delete(lens)
        else:
            box.store(lens)

    def get_score(self):
        return reduce(Box.add_score, self.boxes.values(), 0)

class Lens:
    def __init__(self, data):
        self.delete = data[-1] == '-'
        self.focal_length = None if self.delete else int(data[-1])
        self.label = data[:-1 if self.delete else -2]
        self.hash = reduce(lambda hash, value: ((hash + ord(value)) * 17) % 256, self.label, 0)

    def process(box_collection, data):
        box_collection.process(Lens(data))
        return box_collection


def answer(input_file):
    start = perf_counter_ns()
    with open(input_file, 'r') as input:
        box_collection = reduce(Lens.process, input.read().split(','), BoxCollection())
    answer = box_collection.get_score()
    end = perf_counter_ns()

    print(f'The answer is: {answer}')
    print(f'{((end-start)/1000000):.2f} milliseconds')

input_file = os.path.join(os.path.dirname(__file__), 'input')
answer(input_file)
