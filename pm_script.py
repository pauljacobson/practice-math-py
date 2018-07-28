import math
import random
from operator import add, sub, mul, truediv

count = 0
score = 0

# Create a dictionary with math operators to use in the equation
ops = {
    '+': add, 
    '-': sub,
    '*': mul,
    '/': truediv,
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
    eq1 = eval(f"{num1} {op} {num2}")
    print(eq1)

equations()