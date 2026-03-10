# Filename: S02/fibo-sumN.py

def fibon(n):
    """Calculates the nth Fibonacci term."""
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a

def fibosum(n):
    """Calculates the sum of the first n Fibonacci terms."""
    total_sum = 0
    # Loop from the 1st term to the nth term
    for i in range(n + 1):
        # This function calls another function
        total_sum += fibon(i)
    return total_sum

# Main program calls fibosum twice
print(f"Sum of the First 5 terms of the Fibonacci series: {fibosum(5)}")
print(f"Sum of the First 10 terms of the Fibonacci series: {fibosum(10)}")