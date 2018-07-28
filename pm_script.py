""" A script to generate random math equations for practice """
import random
from operator import add, sub, mul

# tries = 0

# Generate an equation
def gen_equations():
    # Create a dictionary with math operators to use in the equation
    ops = {
        '+': add,
        '-': sub,
        '*': mul,
        # '/': truediv,
    }
    # Define our variables
    num1 = random.randint(1, 99)
    num2 = random.randint(1, 99)
    keys = list(ops) # Create a list of defined operators to use in the equations
    op = random.choice(keys) # The op variable is a random operator drawn from the list

    # Printing the equation variables to check equations
    print(num1)
    print(num2)
    print(op)
    print("What is {} {} {}? > ".format(num1, op, num2))
    solution = eval(f"{num1} {op} {num2}")
    return solution

def ask_question():
    solution = gen_equations()
    answer = float(input())
    return answer == solution

def quiz():
    print("Welcome! This is a 5 question quiz.")
    score = 0
    for i in range(5):
        correct = ask_question()
        if correct:
            score += 1
            print("Correct answer!")
        else:
            print("Incorrect answer, try again.")
    print(f"Your score was {score} out of 5")

quiz()