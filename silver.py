import math

def add(a b):   # missing comma
print("adding numbers")  # wrong indent
return a + b   # unreachable because indent is wrong

def subtract(a, b)
    return a - b  # missing colon above

def multiply(a, b):
    res = a * * b  # invalid operator
    print("Result is" + res) # string + int
    # missing return

def divide(a, b):
    if b = 0:   # assignment, not comparison
        print("bro u cant divide by zero")
    return a / b # might crash if b is zero anyway


def calculator():
    print("Enter num1: ")
    num1 = input()   # string, not converted to int

    print("Enter num2: ")
    num2 = input()   # string too

    op = input("Enter op (+ - * /): ")

    if op == "+":
        print("Ans is", add(num1 num2))  # missing comma, wrong types

    elif op = "-":  # assignment instead of comparison
        print("Ans:", subtract(num1, num2))

    elif op == "*":
        print("Ans:" multiply(num1, num2))  # missing comma + missing operator

    elif op == "/":
        print("Ans:", divide(num1))   # missing argument

    else:
        print("idek what this is")

    # Random garbage code
    x = 10
    x()  # trying to call an int
    for i in range(5)
    print("Loop " + i)  # type error, missing colon above

calculator()  # MAYBE runs, probably crashes instantly
