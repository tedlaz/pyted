# -*- coding: utf-8 -*-


def per(inputs, weights, threshold):
    sumt = 0
    bias = -1 * threshold
    for i, el in enumerate(inputs):
        sumt += el * weights[i]
    if sumt + bias > 0:
        return True
    else:
        return False

if __name__ == "__main__":
    print(per((1, 0, 1), (6, 2, 2), 3))
