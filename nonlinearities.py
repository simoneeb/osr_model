import numpy as np


def p(V,theta= 0):


    """
    rectification function for synapse rectification

    """
    
    if V < theta:
        return 0
    else:
        return (V-theta)
    


def N(V,params):

    """
    piecewise-linear nonlinearity

    """

    slope = params.get('slope',1)
    threshold = params.get('threshold',0)

    
    if V <= threshold:
        return 0
    else:
        return (V-threshold)*slope
    

def sig(x,  slope,threshold,max_val):

    """
    sigmoidal nonlinearity
    
    """

    return max_val/ (1 + np.exp(-slope * (x - threshold)))



# def sig(x,  params):

#     """
#     sigmoidal nonlinearity
    
#     """

#     slope = params.get("slope_inp",9)
#     threshold = params.get("threshold_inp",.5)
#     max_val = params.get("max_val_inp",1)


#     return max_val/ (1 + np.exp(-slope * (x - threshold)))




def tanh(x,  params):

    """
    sigmoidal nonlinearity
    
    """

    slope = params.get('slope_inp',1)
    threshold = params.get('threshold_inp',0)
    max_val = params.get('max_val_inp',0)
    z = slope*(x - threshold)

    #return (np.exp(z)- np.exp(z)) / (np.exp(z) + np.exp(z))
    return np.tanh(z)

