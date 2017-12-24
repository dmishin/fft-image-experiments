import numpy as np

def turn(n):
    """Formula from WIkipedia.
    n could be numpy array of integers
    """
    return (((n & -n) << 1) & n) != 0        

def dragon(N):
    """Generate dragon curve
    Returns a pair of integer arrays, (x,y), each 2^N elements long
    """
    t = turn(np.linspace(0, 2**N-1, 2**N, dtype=np.int32))

    a = np.remainder(np.cumsum(t*2-1), 4)

    #   1 | 0
    #   --+--  
    #   2 | 3
    dx = np.array([1, -1, -1, 1], dtype=np.int32)
    dy = np.array([1, 1, -1, -1], dtype=np.int32)
    
    
    x = np.cumsum(dx[a])
    y = np.cumsum(dy[a])

    return x-((dx-1)//2)[a],y-((dy-1)//2)[a]

def dragon_binary_diagram(N):
    """Draw dragon curve on a bitmap
    Returned bitmap size is 2^N x 2^N
    """
    #Prepare canvas to draw curve
    D = np.zeros((2**N,2**N), dtype=np.float32)
    
    #Get curve. Scale is 2x.
    dx, dy = dragon(2*N-1)

    dx *= 2
    dy *= 2

    #Center the curve.
    cx, cy = (int(dx.mean()), int(dy.mean()))
    x0 = cx - D.shape[0]//2
    y0 = cy - D.shape[1]//2
    dx -= x0
    dy -= y0

    #Given array of coordinates, writes 1 at theese coordinates, when they are inside canvas.
    def putOnesAt(dx,dy):
        inside = (dx >= 0) & (dx < D.shape[0]) & (dy>=0) & (dy<D.shape[0])
        #Take part of x,y coordinates that are inside the image, and write repeated pattern by them
        #
        D[dx[inside],dy[inside]] = 1

    #Draw corners
    putOnesAt(dx,dy)

    #Draw midpoints between corners
    dx1 = (dx[0:-1]+dx[1:])//2
    dy1 = (dy[0:-1]+dy[1:])//2
    putOnesAt(dx1,dy1)
    return D
    

def showdragon(N):
    pp.plot(*(dragon(N)+()))
    pp.show()

if __name__=="__main__":
    from matplotlib import pyplot as pp
    order = 16
    print("Showing dragon curve of order {}".format(order))
    showdragon(order)
