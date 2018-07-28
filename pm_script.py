""" A script to generate random math equations for practice """
import math
import random
from operator import add, sub, mul

tries = 0
score = 0

# Create a dictionary with math operators to use in the equation
ops = {
    '+': add,
    '-': sub,
    '*': mul,
    # '/': truediv,
}

# Define our variables
num1 = random.randint(10, 999)
num2 = random.randint(10, 999)
keys = list(ops) # Create a list of defined operators to use in the equations
op = random.choice(keys) # The op variable is a random operator drawn from the list

# Printing the equation variables to check equations
print(num1)
print(num2)
print(op)

# Generate an equation
def equations():
	# answer = input("What is {} {} {}?".format(num1, op, num2))
	# print(answer)
	# if answer == eval(op(num1, num2)):
		# print("You are correct!")
		# score += 1
    answer = input("What is {} {} {}? > ".format(num1, op, num2))
    solution = eval(f"{num1} {op} {num2}")
    print(f"The correct answer is {solution}")
    if answer == solution:
    	print("Correct answer!")
    else:
    	print("Incorrect, try again")

equations()