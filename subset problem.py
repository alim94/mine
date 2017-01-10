from random import randint, sample
import random
import itertools
from time import time
import math
import sys
#pip install numpy on pip folder from the python folder (shift right click to open command prompt)
#python-> script-> pip
import numpy as np
#uncomment this code to print full matrix rather than the abbreviated one
# np.set_printoptions(threshold=np.nan)
class SSP():
    #initializing the SSP object
    def __init__(self, S=[], t=0):
        self.S = S #empty set to  start with
        self.t = t #target set to 0 initially
        self.n = len(S) #length of the set (i.e. number of elements)
        #
        self.decision = False 
        self.total    = 0
        self.selected = [] #empty set for the selected subset
    def __repr__(self):
        return "SSP instance: S="+str(self.S)+"\tt="+str(self.t)
    
    def random_instance(self, n, bitlength=10):
        max_n_bit_number = 2**bitlength-1
        self.S = sorted( [ randint(0,max_n_bit_number) for i in range(n) ] , reverse=True)
        self.t = randint(0,n*max_n_bit_number)
        self.n = len( self.S )
    #generate random SSP instance which will generate a solution
    def random_yes_instance(self, n, bitlength=10):
        max_n_bit_number = 2**bitlength-1
        #generate a random set of integers of length n
        #and store as reverse sorted
        self.S = sorted( [ randint(0,max_n_bit_number) for i in range(n) ] , reverse=False)
        #set the target value to the sum of a sample subset of the set
        #where the length of the sample set is a randint between 0 and n (4)
        self.t = sum( sample(self.S, randint(0,n)) )
        #set n property of object to length of the set 
        self.n = len( self.S )
        
    #try generating a solution randomly (greedy algorithm)
    def try_at_random(self):
        #initialise a empty set for the candidate
        candidate = []
        #current total of sum of subset
        total = 0
        #whilst the total sum is not equal to target keep trying
        while total != self.t:
            #get a random sample of between 0 and 4 elements to test
            candidate = sample(self.S, randint(0,self.n))
            #evaluate the total of the subset
            total     = sum(candidate)
            print( "Trying: ", candidate, ", sum:", total )
    
    #function to perform the brute force         
    def brute_force(self):
       #calls the function getSubsets to generate all the subsets for the initial set and return the subsets
       subsets =  self.getSubsets()
       total = 0
       #loop through every set of the subsets
       for set in subsets:
            #set the total to equal the sum of the current set
           total = sum(set)
           #print the set that is currently being tested
           print("Trying: ", set, ", sum:", total )
           #if the total does not match the value of t which is the target value then solution has been found
           if (total == self.t):
            #print the solution out
              print("Solution: " +str(set))
              return True
    def dynamic_programming(self):
        set = np.full((self.t+1,self.n+1),-1)
        # print(set)
        #initialises the first row as true
        for i in range(0,self.n+1):
            set[0][i] = True
        #initialises the first column as false
        for j in range(1, self.t+1):
            set[j][0] = False
        #if the row or column value is less than the set value swap false to true otherwise leave it how it is
        for i in range(1, self.t+1):
            for j in range(1, self.n+1):
                set[i][j] = set[i][j-1]
                if (i >= self.S[j-1]):
                    set[i][j] = set[i][j] or set[i - self.S[j-1]][j-1]
        print str(set)
        return set[self.t][self.n]
    def AcceptanceProbability(self, new, old, temp): 
        if new or old is not None:
            if (new < old):
                return 1.0
            else:
                return math.exp((old-new)/temp)
        else:
            return 0
    def GRASP(self, max_iter):
         best_candidate = 0
         while (i <=  max_iter):
             greedy_candidate = GreedyAlgorithm()
             grasp_candidate = LocalSearch(greedy_candidate)
    def local_search(self,greedy_set):
        candidate = []
        for i in range(0, self.n):
            for j in range(0, greedy_set):
                if (self.S[i] not in greedy_set):
                    greedy_set[i]
    def NeigbouringSolution(self, set = []):
        if len(set) != 0:
            randPosSet = randint(0, len(set))
            randPosSet1 = randint(0, len(set)-1)
            set1 = list(set)
            
            if len(self.S) == len(set1):
                print "No Neighbouring Solution"
            else:
                for i in range(0, self.n):
                    if self.S[i] in set1:
                        randPosSet = randint(0, len(set))
                        # print "rand: " + str(randPosSet)
                    else:
                        set1[randPosSet1] = self.S[i]
                        break
            # print("Initial: " +str(set)) 
            # print("Neighbour: " +str(set1) + "\n")
            return set1
    def CalculateCost(self,set):
        if not set:
            return
        else:   
            return sum(set)
        
    def sim_anneal(self):
        solution = self.greedy_algorithm()
        old_cost = self.CalculateCost(solution)
        Temp = 1.0
        TempMin = 0.00001
        alpha = 0.09
        if len(solution) == 0:
            return True
        while Temp > TempMin:
            i = 1
            while i <= 3:
                # print("i: " + str(i))
                solution1 = self.NeigbouringSolution(solution)
                print("Initial Solution: " +str(solution) + " Cost: " + str(old_cost))
                new_cost = self.CalculateCost(solution1)
                print("Neighbouring Solution: " +str(solution1)  + " Cost: " + str(new_cost))
                ap = self.AcceptanceProbability(old_cost, new_cost,Temp)
                if ap > random and sum(solution1) <= self.t:
                    solution = list(solution1)
                    old_cost = new_cost
                i = i + 1
            Temp = Temp*alpha
        return solution
    def greedy_algorithm(self):
        total = 0
        subsets = []
        for i in range(0, len(self.S)):
            if (sum(subsets) + self.S[i]<= self.t):
                subsets.append(self.S[i])
                total = total + self.S[i]
            else:
                print(total-self.t)
                break
        # print ("Greedy: " +str(subsets))
        return subsets
    #function to generate all the subsets of the initial set
    def getSubsets(self):
        #empty array to store all the subsets, len will be equal to 2^n where n is the length of the initial set
        results = []
        #loops through the length of the set and generates a non repeated array of subsets
        for i in range(0,len(self.S)+1):
            #use combinatorics to find all possible non repeated combinations (subsets) of the initial set 
            results += itertools.combinations(self.S,i)
        # #loop through the results array and print all the subsets
        # for x in results:
        #     print(list(x))
        return results
        
instance = SSP() #generate instance of SSP Class and initialise
instance.random_yes_instance(4)
print( instance )
##instance.try_at_random()
#call the brute force method passing in a length  for the array instance to be generated
print("Solution: " +str(instance.sim_anneal()))
instance.greedy_algorithm()
if (instance.dynamic_programming() == True):
    print("Solution Found")
else:
    print("No Solution Found")
