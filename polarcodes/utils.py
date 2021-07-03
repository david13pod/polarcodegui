#!/usr/bin/env python

"""
Math provides miscellaneous math operations to the other classes, which are important for polar codes
algorithm implementations.
"""

import numpy as np
from numpy.lib.function_base import flip

def bit_reversed(x, n):
    """
    Bit-reversal operation.

    Parameters
    ----------
    x: ndarray<int>, int
        a vector of indices
    n: int
        number of bits per index in ``x``

    Returns
    ----------
    ndarray<int>, int
        bit-reversed version of x

    """

    result = 0
    for i in range(n):  # for each bit number
        if (x & (1 << i)):  # if it matches that bit
            result |= (1 << (n - 1 - i))  # set the "opposite" bit in result
    return result

def logdomain_diff(x, y):
    """
    Find the difference between x and y in log-domain. It uses log1p to improve numerical stability.

    Parameters
    ----------
    x: float
        any number in the log-domain
    y: float
        any number in the log-domain

    Returns
    ----------
    float
        the result of x - y

    """

    if x > y:
        z = x + np.log1p(-np.exp(y - x))
    else:
        z = y + np.log1p(-np.exp(x - y))
    return z

def logdomain_sum(x, y):
    """
    Find the addition of x and y in log-domain. It uses log1p to improve numerical stability.

    Parameters
    ----------
    x: float
        any number in the log-domain
    y: float
        any number in the log-domain

    Returns
    ----------
    float
        the result of x + y

    """

    if x > y:
        z = x + np.log1p(np.exp(y - x))
    else:
        z = y + np.log1p(np.exp(x - y))
    return z

def bit_perm(x, p, n):
    """
    Find the permutation of an index.

    Parameters
    ----------
    x: ndarray<int>, int
        a vector of indices
    p: ndarray<int>
        permutation vector, ex: bit-reversal is (0,1,...,n-1)
    n: int
        number of bits per index in ``x``

    Returns
    ----------
    ndarray<int>, int
        permuted indices

    """

    result = 0
    for i in range(n):
        b = (x >> p[i]) & 1
        result ^= (-b ^ result) & (1 << (n - i - 1))
    return result

# find hamming weight of an index x
def hamming_wt(x, n):
    """
    Find the bit-wise hamming weight of an index.

    Parameters
    ----------
    x: int
        an index
    n: int
        number of bits in ``x``

    Returns
    ----------
    int
        bit-wise hamming weight of ``x``

    """

    m = 1
    wt = 0
    for i in range(n):
        b = (x >> i) & m
        if b:
            wt = wt + 1
    return wt

# sort by hamming_wt()
def sort_by_wt(x, n):
    """
    Sort a vector by index hamming weights using hamming_wt().

    Parameters
    ----------
    x: ndarray<int>
        a vector of indices
    n: int
        number of bits per index in ``x``

    Returns
    ----------
    ndarray<int>
        sorted vector

    """

    wts = np.zeros(len(x), dtype=int)
    for i in range(len(x)):
        wts[i] = hamming_wt(x[i], n)
    mask = np.argsort(wts)
    return x[mask]

def inverse_set(F, N):
    """
    Find {0,1,...,N-1}\F. This is useful for finding the information set given a frozen set as ``F``.

    Parameters
    ----------
    F: ndarray<int>
        a vector of indices
    N: int
        block length

    Returns
    ----------
    ndarray<int>
        inverted set as a vector

    """

    n = int(np.log2(N))
    not_F = []
    for i in range(N):
        if i not in F:
            not_F.append(i)
    return np.array(not_F)

def subtract_set(X, Y):
    """
    Subtraction of two sets.

    Parameters
    ----------
    X: ndarray<int>
        a vector of indices
    Y: ndarray<int>
        a vector of indices

    Returns
    ----------
    ndarray<int>
        result of subtracted set as a vector

    """

    X_new = []
    for x in X:
        if x not in Y:
            X_new.append(x)
    return np.array(X_new)

def arikan_gen(n):
    """
    The n-th kronecker product of [[1, 1], [0, 1]], commonly referred to as Arikan's kernel.

    Parameters
    ----------
    n: int
        log2(N), where N is the block length

    Returns
    ----------
    ndarray<int>
        polar code generator matrix

    """

    F = np.array([[1, 1], [0, 1]])
    F_n = F
    for i in range(n - 1):
        F_n = np.kron(F, F_n)
    return F_n

# Gaussian Approximation helper functions:

def phi_residual(x, val):
    return phi(x) - val

def phi(x):
    if x < 10:
        y = -0.4527 * (x ** 0.86) + 0.0218
        y = np.exp(y)
    else:
        y = np.sqrt(3.14159 / x) * (1 - 10 / (7 * x)) * np.exp(-x / 4)
    return y

def phi_inv(y):
    return bisection(y, 0, 10000)

def bisection(val, a, b):
    c = a
    while (b - a) >= 0.01:
        # check if middle point is root
        c = (a + b) / 2
        if (phi_residual(c, val) == 0.0):
            break

        # choose which side to repeat the steps
        if (phi_residual(c, val) * phi_residual(a, val) < 0):
            b = c
        else:
            a = c
    return c

def logQ_Borjesson(x):
    a = 0.339
    b = 5.510
    half_log2pi = 0.5 * np.log(2 * np.pi)
    if x < 0:
        x = -x
        y = -np.log((1 - a) * x + a * np.sqrt(b + x * x)) - (x * x / 2) - half_log2pi
        y = np.log(1 - np.exp(y))
    else:
        y = -np.log((1 - a) * x + a * np.sqrt(b + x * x)) - (x * x / 2) - half_log2pi
    return y

class CRC:
    '''
    Implementation of CRC encoder and decoder/detector
    '''
    def __init__(self, info, crc_n):
        self.info = list(info)
        self.crc_used=True
        # Apply 5G allowed crc polynomials nos
        if crc_n == 0:
            self.crc_used=False
            print ('crc_n have not been added in CRC !')
        elif crc_n == 6:
            loc = [6, 5, 0]
        elif crc_n ==11:
            loc = [11, 10, 9, 5, 0]
        elif crc_n == 24:
            loc = [24, 23, 21, 20, 17, 15, 13, 12, 8, 4, 2, 1, 0]
        else:
            self.crc_used=False
            print ('crc_n have not been added in CRC !')
        
        #create divisor variable
        if self.crc_used != False:
            p = [0 for i in range(crc_n + 1)]
            for i in loc:
                p[i] = 1
            # flip divisor
            p=p[::-1]

            info=self.info.copy()
            times = len(info)

            # append crcn zeros
            for i in range(crc_n):
                info.append(0)

            # result container
            q = []
            for i in range(times):
                if info[i] == 1:
                    q.append(1)
                    for j in range(crc_n+1):
                        info[j + i] = info[j + i] ^ p[j] #XOR operation
                else:
                    q.append(0)

        
            check_code = info[-crc_n::] #reminder as the crc to be added

            # append reminder to infomation bit
            code = self.info.copy()
            for i in check_code:
                code.append(i)

            self.crc_n = crc_n
            self.p = p
            self.q = q
            self.check_code = check_code
            self.code = np.array(code)
        

    def detection(self,decoded_info):
        if self.crc_used != False:
            crc_n=self.crc_n
            divisor=self.p
            coded_info=list(decoded_info.copy())
            info_len=len(coded_info)-crc_n
            qq = []
            for i in range(info_len):
                if coded_info[i] == 1:
                    qq.append(1)
                    for j in range(crc_n+1):
                        coded_info[j + i] = coded_info[j + i] ^ divisor[j]
                else:
                    qq.append(0)

            check_decoded = coded_info[-crc_n::]
            confirm=sum(check_decoded)
            

            if confirm == 0:
                value = 1
                msg=list(decoded_info.copy())[:info_len]
            else:
                value = 0
                msg=list(decoded_info.copy())[:info_len]
            return (value,msg)
        else:
            raise('CRC not used, Detector cannot work')