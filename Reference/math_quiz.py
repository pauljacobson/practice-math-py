# From https://stackoverflow.com/questions/30926323/how-to-do-a-calculation-on-python-with-a-random-operator/30926409

from operator import add, mul, sub
import random

score = 0  # score of user
questions = 0  # number of questions asked
operators = {"+": add, "-": sub, "*": mul}
print("You have now reached the next level!This is a test of your addition and subtraction")
print("You will now be asked ten random questions")
# create list of dict keys to pass to random.choice
keys = list(operators)
# use range 
for _ in range(10):  
    number1 = random.randint(1, 20)
    number2 = random.randint(1, 20)
    operator = random.choice(keys)
    # cast answer to int, operators[operator]will be either add, mul or sub
    # which we then call on number1 and number2
    answer = int(input("What is {} {} {}?".format(number1,operator, number2)))
    if answer == (operators[operator](number1, number2)):
        print("You are correct")
        score += 1
    else:
        print("incorrect")