class sumfitnesses:
    # this class is only used to get the average fitness of each enemy generation and return them to be displayed by matplotlib
    def __init__(self):
        # declare lists used in calculation
        self.generation = []
        self.nums = []

    def sumfitnesses(self, nums, generation):
        self.generation = generation
        self.nums = nums
        # this is for debugging in order to checck to see if the fitness value averages calculated match with the hand taken averages
        #print(self.generation)
        #print(self.nums)
        runningTotal = 0 # the current sum of numbers in this generation
        counter = 0 # the amount of numbers summed
        means = [] # the list of means, this is what is returned by the function at the end
        for i in range(len(self.generation)): # for the length of the list of generations
            if i == 0: # always add the first number as the check to see if its in the same generation will cause an error if used on value 0 as it will try check value -1
                runningTotal += self.nums[i] # add first value to the running total and set the counter to 1
                counter = 1
                continue # go to next iteration
            elif self.generation[i-1] == self.generation[i]: # if the previous generation value is equal to the current one then add to running total and increment counter
                runningTotal += self.nums[i]
                counter += 1
            else: # if the value of current generation isnt the same as the last one then calculate the mean and add it to the list of means
                means.append(runningTotal/counter)
                runningTotal = self.nums[i] # set the running total to the current number
                counter = 1 # reset counter to 1
        means.append(runningTotal/counter) # add the final mean to the list, without this the last mean would never be added to the list as the last else would never be reached
        return means # return the means list
            
