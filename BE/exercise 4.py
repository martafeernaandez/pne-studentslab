score = input("Enter your score: ")

for score in score.split():
    if 9 <= float(score) <= 10:
        print("A")
    elif 7 <= float(score) <= 8.9:
        print("B")
    elif 5 <= float(score) <= 6.9:
        print("C")
    elif 3 <= float(score) <= 4.9:
        print("D")
    elif 0 <= float(score) <= 2.9:
        print("E")

print("Score 9.5:", score)
print("Score 7:", score)
print("Score 5.5: ", score)
print("Score 3.3:", score)
print("Score 1:", score)