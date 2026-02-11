temperatures = [15.5, 17.2, 14.8, 16.0, 18.3, 20.1, 19.5]

print("Wednesday: ", temperatures[2])
print("Max: ", max(temperatures))
print("Min: ", min(temperatures))
print("Average: ", sum(temperatures) / len(temperatures))

print("Days above 17: ", sum(1 for t in temperatures if t > 17))
print("Sorted: ", sorted(temperatures))