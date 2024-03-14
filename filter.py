import numpy as np


#filter function 
def filter_exponential(t,tau):
   
    kernel =   np.exp(-t/tau) * np.heaviside(t,1)

    return kernel



def filter_alpha(t,tau):
   
    kernel =  (t/tau) * np.exp(-t/tau) * np.heaviside(t,1) 

    return kernel


def filter_alpha_norm(t,tau):

    """
    tau**2 because normalized to have intergal = 1

    """
    kernel =  (t/tau**2) * np.exp(-t/tau) * np.heaviside(t,1) 

    return kernel


def filter_biphasic_norm(t,tau_B, tau_A, SF_A):

    kernel =  (t/tau_B**2) * np.exp(-t/tau_B) * np.heaviside(t,1) -  SF_A * (t/tau_A**2) * np.exp(-t/tau_A) * np.heaviside(t,1) 

    return kernel