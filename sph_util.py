# -*- coding: utf-8 -*-
r"""
sph_util
========

a bunch of useful definitions
"""
import numpy as np
import sys
import matplotlib.pyplot as plt # currently used only by the 'fit_histgauss' function and would easily be commented to get rid of matplotlib 
#import scipy.stats

########################################

class SPH_index:
    r"""
    an index is used to read values in a ndarray. It can be an int or a list of int. attributs: _index (int or list of int), _listindex (list)
    """
    def __init__(self,index=None,minindex=None,maxindex=None,kind=None,convention='max+1'):
        r"""
        Parameters
        ----------
            index: 3 possibilities: 1. int (min/max are ignored) ; 2. list of int (min/max are ignored) ; 3. anything (min/max must be defined)
                if index is a list, every element must be int. not verified to save CPU !!!
            minindex, maxindex: ints corresponding to a minimum and a maximum. if index is neither an int or a list, minmax are used to make a range
            kind: string that may give the kind
            convention: default 'max+1' means the old convention where the max value belongs to the list
                othrerwise convention can be anything
                
        Examples
        -------
            >>> i=SPH_index(index=1,kind='time')
            >>> i=SPH_index(minindex=0,maxindex=10)
            >>> i=SPH_index(minindex=0,maxindex=10,convention=0)
        """
        self._index = index # previous '_' convention kept for compatibility
        if isinstance(index,int):
            self._listindex = [index]
        elif isinstance(index,list):# if index is a list, no test that every single element is an int !!! to be added later if necessary but it seems to me uelessly CPU consuming
            self._listindex = index
        else:
            if convention == 'max+1':
                self._listindex = list(range(minindex,maxindex+1))
            else:
                self._listindex = list(range(minindex,maxindex))
        self.kind = kind
        self.index = self._index
        self.listindex = self._listindex
####################################
def sum_gauss1D(x, amplitude=1, meanx=0, sigma=1, tau=None, Ngauss=1):
    r"""
    sum of Ngauss 1D-gaussians normalised such as the max is equal to sum(amplitude)
    ==> integrale==sum( sqrt(2*pi)*sigma*amplitude )
    amplitude, meanx, sigma/tau can be numbers (in this case all Ngauss take this value), lists of Ngauss numbers or ndarrays of Ngauss numbers
    Parameters
    ----------
        x: float or ndarray
            x value(s) where the sum is calculated
            
        amplitude: float or 1D-ndarray
            amplitudes, default 1

        meanx: float or 1D-ndarray
            centers, default 0

        sigma: float or 1D-ndarray >0
            standard deviations, default 1

        tau: None, float or 1D-ndarray >0
            precisions, tau=1/sigma**2. by default, tau is none and the sum is computed according to sigma. if tau is given then the sum is computed according to tau and sigma is ignored
        
         
    Returns
    -------
       y(x): float or ndarray

    Example
    -------
        >>> y = sum_gauss1D(x,amplitude=[1,0.7],meanx=[1,1.5],sigma=[2,3.5])
        
    """
    if isinstance(amplitude,np.ndarray):
        amp = amplitude
    elif isinstance(amplitude,list):        
        amp = np.array(amplitude)
    else:# implicitely just a number
        amp = np.array([amplitude]*Ngauss)
        
    if isinstance(meanx,np.ndarray):
        mu = meanx
    elif isinstance(meanx,list):        
        mu = np.array(meanx)
    else:# implicitely just a number
        mu = np.array([meanx]*Ngauss)
        
# todo: check sigma, tau >0
    if tau is None:
        if isinstance(sigma,np.ndarray):
            to = 1/sigma**2
        elif isinstance(sigma,list):        
            to = 1/np.array(sigma)**2
        else:# implicitely just a number
            to = 1/np.array([sigma]*Ngauss)**2
    elif isinstance(tau,np.ndarray):
        to = tau
    elif isinstance(tau,list):
        to = np.array(tau)
    else:# implicitely just a number
        to = np.array([tau]*Ngauss)
    
    y=np.zeros([len(x)])
    for i in range(Ngauss):
#        import pdb
#        pdb.set_trace()
        y += amp[i] * np.exp(-to[i] * (x - mu[i])**2 / 2)
    return y
###########################################
def gauss2D(x,y,amplitude=1,meanx=0,meany=0,
            sigmamaj=1,sigmamin=1,theta=0):
    r"""
    equation of a 2D-gaussian normalised such as the max is equal to 'amplitude'
    ==> integrale2D == 2*pi * sigmamaj * sigmamin * amplitude
    
    Parameters
    ----------
        sigmamaj, sigmamin: floats
            standard deviations along major and minor axes
            
        theta: float (in radians !!!)
            angle between the x-axis and the major axis
            
        meanx, meany: mean values (ie. centers) of x and y
        
        x,y: floats or ndarrays of the same shape (otherwise ?)
    """
    a = (np.cos(theta))**2/2/sigmamaj**2 + \
        (np.sin(theta))**2/2/sigmamin**2
    b = np.sin(2*theta)/4/sigmamaj**2 - \
        np.sin(2*theta)/4/sigmamin**2
    c = (np.sin(theta))**2/2/sigmamaj**2 + \
        (np.cos(theta))**2/2/sigmamin**2
 
    #z = amp * exp(-a*(x-xm)**2 - 2*b*(x-xm)*(y-ym) - c*(y-ym)**2 )
    z = sum_gauss1D(x,amplitude=amplitude,meanx=meanx,tau=2*a) *\
        sum_gauss1D(x,amplitude=1,meanx=meany,tau=2*c) *\
        np.exp(-2*b*(x-meanx)*(y-meany))
    
    return z
#########################################
def fit_histgauss(data,nbins=100,range=None,color_hist='g',color_gauss='r',
                  normed=True,
                  plot_hist=True,plot_fit=True,write_fit=True,write_stats=True):
    r"""
    ...TBC...
    to fit a sum of gaussians and possibly a bkg on a 1D-histogram
    - possible to plot the histogram
    - possible to overplot the fit in red
    - possible to write parameters of the fit
    - possible to write some statistics
    the fit uses kmpfit (scipy.optimize sucks and the methods proposed in the library doesn't converge as soon the fit is a bit complex).
    all options of plt.hist or np.histogram
    Parameters
    ----------
       ...TBC...
       data : 
       nbins : 
       range : default min/max of the histogram. the fit is performed only on data inside the range
       color_histo : default 'g'
       color_gauss : default 'r'
       plot_hist : boolean, default True
       plot_fit : boolean, default True
       write_fit : boolean, default True
       write_stats : boolean, default True
    """
    compute_fit = plot_fit or write_fit
    compute_stats = compute_fit or write_stats
    if plot_hist:
        compute_histogram = plt.hist
    else:
        compute_histogram = np.histogram
    h = compute_histogram(data,bins=nbins,range=range,color=color_hist,
                          normed=normed)
    if compute_stats:
        median0,mean0,stddev0 = basicstats_hist(h)
    
    
#    params, cov = curve_fit(gauss1D, x, h[0], p0 = [ max(h[0]), mean_init , stddev_init])
#    y = gauss1D(x, *params)
#    #modif 150509
#    #plt.plot(x,y, label='fit', linewidth=4, color='r')
#    pylab.plot(x,y, label='fit', linewidth=4, color=col_gauss)
#    comment = 'mean: ' + str('%.04f'%params[1])
#    pylab.figtext(.75,.85,comment)
#    comment = 'stddev: ' + str('%.04f'%params[2])
#    pylab.figtext(.75,.8,comment)
#    ############
#    return params
#######################################
def basicstats_hist(histo):
    r"""
    ...TBC...
    returns some basic stats computed over the histogram
    """
    j = (histo[1][:-1]+histo[1][1:])/2*histo[0]
    return np.median(j),np.mean(j),np.std(j)
#######################################
def sph_minmax(array): # TBV !!! not sure it is really works...
    r"""
    Computes efficiently the minimum and maximum values of an array (in one pass and with only 1.5*len(array) comparisons, instead of 2*len(array) as found most of the time). see http://code.activestate.com/recipes/577916-fast-minmax-function
    
    Parameters
    ----------
        array: ndarray
           where to look for min & max 

    Returns
    -------
        min, max: same than input
           minimum & maximum values of the array

    Example
    -------
        minimum, maximum = sph_minmax(array)
    """
    if sys.version_info[0]>2:
    # for Python 3
        from itertools import zip_longest
        zzip = zip_longest
    else:
    # for Python 2   
        from itertools import izip_longest
        zzip = izip_longest
    it = iter(array)
    try:
        lo = hi = next(it)
    except StopIteration:
        raise ValueError('error (empty argument ?)')
    for x, y in zzip(it, it, fillvalue=lo):
        if x > y:
            x, y = y, x
        if x < lo:
            lo = x
        if y > hi:
            hi = y
    return lo, hi

