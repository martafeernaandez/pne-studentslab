# Filename: S02/fiboN.py

def fibon(n):
    """Calculates the nth Fibonacci term and returns it."""
    a = 0
    b = 1
    # We loop n times to reach the desired position
    for i in range(n):
        a, b = b, a + b
    return a

# Main program
# Calling the function for the 5th, 10th, and 15th terms
print(f"5th Fibonacci term: {fibon(5)}")
print(f"10th Fibonacci term: {fibon(10)}")
print(f"15th Fibonacci term: {fibon(15)}")