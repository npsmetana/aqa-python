from fibo import generateFibonacci


def test_fibo():
    expected_val = list([1, 1, 2, 3, 5, 8])
    generated_val = generateFibonacci(6)
    print("\ntest_fibo has been run\n")
    assert generated_val == expected_val

