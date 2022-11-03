from time import time
import numpy as np
from Levenshtein import ratio
import ctypes as ctp


def my_lev(a, b):
    # Initialize Matrix
    distances = np.zeros((len(a) + 1, len(b) + 1))
    for a1 in range(len(a) + 1):
        distances[a1][0] = a1
    for b1 in range(len(b) + 1):
        distances[0][b1] = b1

    for a1 in range(1, len(a) + 1):
        for b1 in range(1, len(b) + 1):
            if a[a1-1] == b[b1-1]:
                distances[a1][b1] = distances[a1 - 1][b1 - 1]
            else:
                x = [   distances[a1][b1 - 1],
                        distances[a1 - 1][b1],
                        distances[a1 - 1][b1 - 1]]

                distances[a1][b1] = min(x) + 1

    return distances[len(a)][len(b)]
def my_fast_lev(a, b, threshold):
    # Initialize Matrix
    distances = np.zeros((len(a) + 1, len(b) + 1))
    for a1 in range(len(a) + 1):
        distances[a1][0] = a1
    for b1 in range(len(b) + 1):
        distances[0][b1] = b1

    for a1 in range(1, len(a) + 1):
        for b1 in range(1, len(b) + 1):
            if a[a1-1] == b[b1-1]:
                distances[a1][b1] = distances[a1 - 1][b1 - 1]
            else:
                x = [   distances[a1][b1 - 1],
                        distances[a1 - 1][b1],
                        distances[a1 - 1][b1 - 1]]

                distances[a1][b1] = min(x) + 1

        if min(distances[a1]) > threshold:
            return False

    return True

            
emails = []
with open('C_Tests/test.txt', 'r') as in_file:
    emails = in_file.read().split('\n')
    start = time()
    for i in range(1, len(emails)):
        a = emails[i-1]
        b = emails[i]
        threshold = -1
        if len(a) > len(b):
            threshold = float(len(a))
        else:
            threshold = float(len(b))
        threshold = int(threshold - threshold * .8)
        out = my_fast_lev(a, b, threshold=threshold)

        emails[i] += '      ' + str(out)

    end = time()
    print('Python: ', end-start)

    start = time()
    MyLev = ctp.cdll.LoadLibrary('./my_lib.so').MyLev
    MyLev.argtypes = [ctp.c_char_p, ctp.c_char_p, ctp.c_uint]
    for i in range(1, len(emails)):
        a = emails[i-1]
        b = emails[i]

        a1 = a.encode('utf8')
        b1 = b.encode('utf8')

        out = MyLev(a1, b1, 2)

        emails[i] += '      ' + str(out)

    end = time()
    print('C: ', end-start)


    start = time()
    for i in range(1, len(emails)):
        a = emails[i-1]
        b = emails[i]
        out = ratio(a, b)

        emails[i] += '      ' + str(out)

    end = time()
    print('Old Method: ', end-start)

with open('C_Tests/out_test.txt', 'w') as out_file:
    for e in emails:
        out_file.write(e + '\n')


# start = time()
# out1 = []
# for i in range(1_000_000_0):
#     a = 7
#     b = 12
#     c = 19
#     out1.append(min(a, b, c))

# end = time()
# print('Option 1 took', end - start, 'seconds')

# start = time()
# out2 = []
# for i in range(1_000_000_0):
#     a = [7,12,19]
#     out1.append(min(a))
# end = time()
# print('Option 2 took', end - start, 'seconds')