""" A script to generate random math equations for practice """
import random
from operator import add, sub, mul, truediv

# tries = 0

# Generate an equation
def gen_equations():
    # Create a dictionary with math operators to use in the equation
    ops = {
        '+': add,
        '-': sub,
        '*': mul,
        '/': truediv,
    }
    # Define our variables
    num1 = random.randint(1, 99)
    num2 = random.randint(1, 99)
    keys = list(ops) # Create a list of defined operators to use in the equations
    op = random.choice(keys) # The op variable is a random operator drawn from the list

    # Printing the equation variables to check equations
    print("\nThis is for troubleshooting purposes only:")
    print(num1)
    print(num2)
    print(op)
    print("\nWhat is {} {} {}? > ".format(num1, op, num2))
    solution = round(eval(f"{num1} {op} {num2}"), 2)
    print(solution)
    if solution > 0:
        return solution
    else:
        gen_equations()

def ask_question():
    solution = gen_equations()
    answer = float(input()) # The function doesn't account for non-integer answers
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
			# I want to state the correct answer in the event the user gives the incorrect one
            print(f"Incorrect answer, the correct answer was ....")
    print(f"\nYour score was {score} out of 5")

quiz()