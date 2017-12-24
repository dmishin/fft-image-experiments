from math import pi, log, sqrt
from numpy import array, hstack, vstack
import numpy as np

def hilbert_indices(N):
    """Genrate 2^N x 2^N integer array, filled with values from 0 to 4^N along hilbert curve"""
    m = array([[0]], dtype=np.int)
    for i in range(N):
        d = 4**i
        m1 = vstack((hstack((m.T, m.T[::-1, ::-1] + 3*d)),
                      hstack((m+d, m+2*d))
                 )
       )
        m = m1
    return m

def hilbert_binary_diagram(N):
    """Generate 2^N x 2^N array of 0 and 1, drawing Hilbert curve"""    
    m = array([[1,0],
               [0,0]], dtype = np.uint8)
    for i in range(1, N):
        
        a = 2**i
        m1 = np.zeros((2*a, 2*a), dtype = m.dtype)
        
        m1[0:a, 0:a] = m.T
        m1[a:2*a, 0:a] = m
        m1[a:2*a, a:2*a] = m
        m1[0:a, a:(2*a-1) ] = m.T[:, a-2::-1]
        
        #put additional ones
        m1[a-1,0] = 1
        m1[a, a-1] = 1
        m1[a-1, 2*a-2] = 1

        m = m1
    return m

