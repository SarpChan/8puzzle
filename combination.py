import itertools

with open("test.txt", mode="w") as file:
    origin = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    for i in itertools.permutations("012345678", 9):
        file.write(str(i) + "\n")
