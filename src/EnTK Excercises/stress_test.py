import time
import os

#This is a simple program to find the sum of the numbers 1 to 1,000



def findSum(x):
    sum = 0

    for i in range (x):
	sum = sum + i 
	
    return sum
    	

if __name__ == '__main__':
    start_time = time.time()
    findSum(1000)
    excution_time = time.time()-start_time
    
