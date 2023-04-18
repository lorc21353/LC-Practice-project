from random import *

class sumfitnesses:
    
    def __init__(self):
        self.generation = []
        self.nums = []

    def sumfitnesses(self, nums, generation):
        self.generation = generation
        self.nums = nums
        print(self.generation)
        print(self.nums)
        runningTotal = 0
        counter = 0
        means = []
        for i in range(len(self.generation)):
            if i == 0:
                runningTotal += self.nums[i]
                counter = 1
                continue
            elif self.generation[i-1] == self.generation[i]:
                runningTotal += self.nums[i]
                counter += 1
            else:
                means.append(runningTotal/counter)
                runningTotal = self.nums[i]
                counter = 1
        means.append(runningTotal/counter)
        return means
            
