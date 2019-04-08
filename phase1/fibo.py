def generateFibonacci(length):
    s_fibo = [1]
    prev_member = 0
    cur_member = 1

    if length < 1:
        return list()

    i = 1
    while i < length:
        i += 1
        temp_prev_member = cur_member
        cur_member = cur_member + prev_member
        prev_member = temp_prev_member
        s_fibo.append(cur_member)

    return s_fibo
