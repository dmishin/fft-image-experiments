from hilbert import *

import unittest
class TestHilbertBinary(unittest.TestCase):
    def test_order_1(self):
        m = hilbert_binary_diagram(1)
        exp = [[1,0],
               [0,0]]
        self.assertTrue( (m==exp).all(), "Returned:\n{m},\nExpected:\n{exp}".format(m=m, exp=exp))
    def test_order_2(self):
        m = hilbert_binary_diagram(2)
        exp = [[1,0,1,0],
               [1,0,1,0],
               [1,1,1,0],
               [0,0,0,0]]
        self.assertTrue( (m==exp).all(), "Returned:\n{m},\nExpected:\n{exp}".format(m=m, exp=exp))
    def test_order_3(self):
        m = hilbert_binary_diagram(3)
        exp = [[1,1,1,0,1,1,1,0],
               [0,0,1,0,1,0,0,0],
               [1,1,1,0,1,1,1,0],
               [1,0,0,0,0,0,1,0],
               [1,0,1,1,1,0,1,0],
               [1,0,1,0,1,0,1,0],
               [1,1,1,0,1,1,1,0],
               [0,0,0,0,0,0,0,0]]
        self.assertTrue( (m==exp).all(), "Returned:\n{m},\nExpected:\n{exp}".format(m=m, exp=exp))

class TestHilbertIndex(unittest.TestCase):
    def test_hilbert_indices0(self):
        m = hilbert_indices(0)
        me = array( [[0]], dtype=np.int )        
        self.assertEqual( m, me )
    def test_hilbert_indices1(self):
        m = hilbert_indices(1)
        me = array( [[0,3],
                     [1,2]], 
                    dtype=np.int )        
        self.assertTrue( (m == me).all() ) 
        
    def test_hilbert_indices2(self):
        m = hilbert_indices(2)
        me = array( [[0,1,14,15],
                     [3,2,13,12],
                     [4,7,8,11],
                     [5,6,9,10]], 
                    dtype=np.int )        
        self.assertTrue( (m == me).all(), "returned: \n{m}, expected: \n{me}".format(m=m,me=me) ) 

    def test_hilbert_indicesN(self):
        N = 6
        m = hilbert_indices(N)
        x,y = 0,0
        for i in range(4**N-1):
            self.assertEqual( m[x,y], i, "m[{x},{y}]=={i}".format(**locals()))
            
            found = False
            for dx, dy in [(-1,0),(1,0),(0,1),(0,-1)]:
                x1 = x+dx
                y1 = y+dy
                if x1 < 0 or x1 >= 2**N: continue
                if y1 < 0 or y1 >= 2**N: continue
                if m[x1,y1] == i+1:
                    found = True
                    break
            self.assertTrue(found, "not found neighbor {i} for {x}, {y}".format(**locals()))
            x,y = x1,y1
            
        
