from binascii import hexlify, unhexlify
from time import time
from hashlib import sha256
import numpy as np
from collections import Counter


def find_most_popular(items: list, n: int = 2, j: int = 1):
    if len(items) < n:
        return None, n

    distribution = Counter(items).most_common(n)

    if len(distribution) == 1:
        return distribution[0][0], distribution[0][1]

    if distribution[0][1] == distribution[1][1]:
        return None, len(items) + j
    else:
        if distribution[0][1] >= n:
            return distribution[0][0], distribution[0][1]
        else:
            return None, len(items) + j


def create_mapping_table(b : int, n: int, nodes: list = None):
    if nodes is None:
        nodes = [i for i in range(1, n+1)]
    mappings = latin_square_design(n, nodes)

    if b <= len(mappings):
        return mappings[0:b]

    else:
        repeat = b // len(mappings)
        residual = b % len(mappings)

        result = []
        for i in range(repeat):
            for j in range(len(mappings)):
                result.append(mappings[j])

        for i in range(residual):
            result.append(mappings[i])

        return result


def latin_square_design(n: int, nodes: list):
    x = 0
    y = 3
    result = []
    odd = False

    if n % 2 != 0:
        n -= 1
        odd = True

    for i in range(1, n + 1):
        tmp = []
        if i < 3:
            start = i
        elif i % 2 != 0:
            start = n - x
            x += 1
        else:
            start = y
            y += 1
        tmp.append(nodes[start-1])

        for i in range(n - 1):
            start += 1
            if start > n:
                start = 1

            tmp.append(nodes[start-1])

        result.append(tmp)
    if odd:
        tmp = np.ones(n, dtype=int) * (nodes[n])
        result.append(tmp)

    return np.array(result).T.tolist()


def find_element(element, arr):
    for idx, val in enumerate(arr):
        if val == element:
            return idx
    return -1


def c2s(msg):
    return str(hexlify(msg), encoding='utf8')


def c2b(msg):
    return unhexlify(bytes(msg, encoding='utf8'))


def get_current_time():
    return int(time())


def get_time_difference(given_time):
    return int(given_time - time())


def hash_msg(msg):
    return sha256(msg).digest()







