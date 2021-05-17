# O(n!) algorithm
import math

def factorial(n):
    for x in range(1, math.factorial(int(n))):
        print("Iteration: " + str(x))

num = 12
factorial(num)