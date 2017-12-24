import numpy as np
from matplotlib import pyplot as pp
from math import pi, sqrt

class Turtle:
    def __init__(self, angle_step):
        self.angle_step = angle_step

        self.direction = 0
        
        self.angles = []
        self.directions = []

    def left(self): self.direction -= 1
    def right(self): self.direction += 1
    def forward(self):
        self.angles.append(self.direction)
        self.directions.append(1)
    def backward(self):
        self.angles.append(self.direction)
        self.directions.append(-1)
        

    def produce(self):
        a = np.array(self.angles)*self.angle_step
        d = np.array(self.directions)
        
        dx = np.cos(a) * d
        dy = np.sin(a) * d

        return np.cumsum(dx), np.cumsum(dy)

def gosper(level):
    g = Gosper()
    g.A(level)
    return g.produce()

class Gosper:
    """L-system is:
    A -> A-B--B+A++AA+B-
    B -> +A-BB--B-A++A+B
    """
    def __init__(self):
        self.turtle = Turtle(pi/3)

    def produce(self):
        return self.turtle.produce()
    
    def A(self, level):
        """A -> A-B--B+A++AA+B-"""
        if level == 0:
            self.turtle.forward()
        else:
            t = self.turtle
            level -= 1
            self.A(level)
            t.left()
            self.B(level)
            t.left()
            t.left()
            self.B(level)
            t.right()
            self.A(level)
            t.right()
            t.right()
            self.A(level)
            self.A(level)
            t.right()
            self.B(level)
            t.left()

    def B(self, level):
        """+A-BB--B-A++A+B"""
        if level == 0:
            self.turtle.forward()
        else:
            t = self.turtle
            level -= 1
            t.right()
            self.A(level)
            t.left()
            self.B(level)
            self.B(level)
            t.left()
            t.left()
            self.B(level)
            t.left()
            self.A(level)
            t.right()
            t.right()
            self.A(level)
            t.right()
            self.B(level)

### copied from https://stackoverflow.com/questions/31638651/how-can-i-draw-lines-into-numpy-arrays    
def naive_line(r0, c0, r1, c1):
    import numpy as np
    # The algorithm below works fine if c1 >= c0 and c1-c0 >= abs(r1-r0).
    # If either of these cases are violated, do some switches.
    if abs(c1-c0) < abs(r1-r0):
        # Switch x and y, and switch again when returning.
        xx, yy, val = naive_line(c0, r0, c1, r1)
        return (yy, xx, val)

    # At this point we know that the distance in columns (x) is greater
    # than that in rows (y). Possibly one more switch if c0 > c1.
    if c0 > c1:
        return naive_line(r1, c1, r0, c0)

    # We write y as a function of x, because the slope is always <= 1
    # (in absolute value)
    x = np.arange(c0, c1+1, dtype=float)
    y = x * (r1-r0) / (c1-c0) + (c1*r0-c0*r1) / (c1-c0)

    valbot = np.floor(y)-y+1
    valtop = y-np.floor(y)

    return (np.concatenate((np.floor(y), np.floor(y)+1)).astype(int), np.concatenate((x,x)).astype(int),
            np.concatenate((valbot, valtop)))    

def gosper_diagram(size, order, scale):
    from PIL import Image, ImageDraw
    
    xx,yy = gosper(order)
    xx *= scale
    yy *= scale
    
    xx += int(size/2 - xx.mean())
    yy += int(size/2 - yy.mean())

    image = Image.new("L", (size,size))
    draw = ImageDraw.Draw(image)
    
    draw.line( list(zip(xx,yy)), fill=255 )
    #image.show()    
    return np.asarray(image)

            
if __name__=="__main__":
    print(gosper_diagram( 512, 5, 4*sqrt(1.5)))
        
