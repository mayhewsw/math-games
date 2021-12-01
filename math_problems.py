import random 
operators = [
    (lambda a,b: a+b, "+"),
    # (lambda a,b: a*b, "x")
]

def get_math_problem():
    num1 = random.choice(range(1,11))
    num2 = random.choice(range(1,11))
    operator_func, operator_string = random.choice(operators)
    math_text = f"{num1} {operator_string} {num2}"
    return math_text, operator_func(num1, num2)