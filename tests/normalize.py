# -*- coding: utf-8 -*-


def normalize(value, minv, maxv):
    dif = float(maxv - minv)
    return ((2 * (value - minv)) - dif) / dif


def denormalize(value, minv, maxv):
    dif = float(maxv - minv)
    return .5 * (value + 1) * dif + minv


if __name__ == '__main__':
    print(normalize(1, 1, 5))
    print(denormalize(0, 0, 100))
