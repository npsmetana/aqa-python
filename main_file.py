from fibo import generateFibonacci


def main():
    for i in range(1, 9):
        print("\n\nFibonacci sequence with length ", i, ":\n", generateFibonacci(i))


main()