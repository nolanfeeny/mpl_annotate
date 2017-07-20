# mpl_annotate
Annotation tool for matplotlib figures

Click on figure to create a point (with x and y coordinates saved), drag existing points to update their locations.
Works for images, plots, or any other matplotlib figure.

## INSTRUCTIONS:
download or copy & paste "annotate.py"

In Jupyter Notebooks:

cell [1] 

    !pip3 install mpld3 --- AFTER RUNNING ONCE, DON'T RUN AGAIN OR CLONE

cell [2] 

    # only needs to be run after kernel has restarted
    import sys
    sys.path.append('./packages')
    %matplotlib inline
    import annotate
    import scipy.misc as misc
    import matplotlib.pylab as plt
    
cell [3] 

    im = misc.imread('sample_image.jpg')
    fig = plt.figure(figsize=(10,7))
    plt.imshow(im, origin='lower')
    annotate.pickpoints(color='cyan', radius=2) # default is color='white', radius=4
    
cell [4] 
    
    print(x,y) # for x and y locations for each point
               # for cleaner format, print(annotate.cleanformat(x))
