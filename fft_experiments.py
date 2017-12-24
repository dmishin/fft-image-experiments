from math import pi, log, sqrt
from numpy import array, hstack, vstack, clip, histogram
from numpy.fft import fft2,fftshift
from PIL import Image
import numpy as np

def value_diapason(x, percent=0.95, nbins=100):
    """Use histogram to determine interval, covering 95% of values"""
    counts, bins = histogram(x.ravel(),nbins)
    total = sum(counts)
    accum = 0
    low = bins[-1]
    high = bins[0]
    #enumerate histogram bins starting from the most populated. 
    for i, cnt in sorted(enumerate(counts), 
                          key = (lambda i_c: i_c[1]),
                          reverse=True):
        accum += cnt
        low = min(low, bins[i])
        high = max(high, bins[i+1])
        if accum > percent * total:
            break
    return low, high
    

def toimage(fimg, gamma=1.9, percent=0.95, extend = 1.1, save=None):
    """Show binary matrix as monochrome image, automatically detecting upper and lower brightness bounds
    """
    low, high = value_diapason(fimg, percent=percent)

    mid = (low+high)/2
    low = mid + (low-mid)*extend
    high = mid + (high-mid)*extend
    
    image = Image.fromarray((clip((fimg-low)/(high-low),0,1)**gamma*255).astype(np.uint8), "P")
    if save is not None:
        image.save(save)
        print("Saving image file: {}".format(save))
    return image



if __name__=="__main__":
    N = 10

    #Hilbert curves
    print("Hilbert curve experiment")
    if True:
        from hilbert import hilbert_indices, hilbert_binary_diagram

        #The patter that will be put along the image
        pattern = np.array([1,1,-1,-1])
        
        H = hilbert_indices(N)
        #Fill hilbert curve with repeating pattern
        img = pattern[(H%len(pattern))]
        toimage(img, gamma = 1.0,
                save = "hilbert-pattern-order{}.png".format(N))

        fimg = np.log(np.abs(fft2(img))+1e-100)
        toimage(-fimg, gamma = 1, percent=0.7, extend = 1.5,
                save = "hilbert-pattern-order{}-fft-inverted.png".format(N))


        img = hilbert_binary_diagram(N)
        toimage(img, gamma = 1.0,
                save = "hilbert-curve-order{}.png".format(N))

        fimg = np.log(np.abs(fft2(img))+1e-100)
        toimage(-fimg, gamma = 1, percent=0.7, extend = 1.5,
                save =  "hilbert-curve-order{}-fft-inverted.png".format(N))

    #Dragon curve
    print("Dragon curve experiment")
    if True:
        from dragon import dragon_binary_diagram
        D = dragon_binary_diagram(N)#toimage(D).show()

        toimage(D, save="dragon_diagram_{}.png".format(N))
        
        fimg = np.log(np.abs(fft2(D))+1e-100)
        toimage(fftshift(fimg),
                save="dragon_diagram_{}_fft.png".format(N)
        )
        
    #gosper curve
    print("Gosper curve experiment")
    if True:
        from gosper import gosper_diagram
        size = 2**N
        scale = 4
        #calculate the order using the fact that curve increases by sqrt(7) times
        order = int(log(size/scale)/log(sqrt(7)))
                
        img = gosper_diagram( size, order, scale=scale )
        toimage(img, save="gosper_diagram_{}.png".format(size))
        
        fimg = np.log(np.abs(fft2(img))+1e-100)
        toimage(fftshift(fimg),
                save="gosper_diagram_{}_fft.png".format(size))
