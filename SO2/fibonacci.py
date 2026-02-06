# Filename: S02/fibonacci.py

a = 0
b = 1

# We use a simple loop instead of a function
for i in range(11):
    # Print the current term
    print(a, end=" ")

    # Update values for the next iteration
    # This is the 'Fibonacci logic': a becomes b, b becomes a + b
    a, b = b, a + b