

import numpy as np



def design_matrix_1D(stimulus,td):

    '''

    return matrix containing one row for each simuation timepoit
    containing the preceeding stimulus of the same length as the filter (td)
    
    '''
    
    stimulus_timesteps = stimulus.shape[0]+td
    
    
    stimulus_padded = np.concatenate((np.zeros(td),stimulus))
    X = np.zeros((stimulus_timesteps,td))
    
    for t in range(stimulus_timesteps):
        if t < td:
            continue
        else:
            X[t,:] = stimulus_padded[t-td:t]
    
        
    return X[td+1:,:]
    
 

#function to convolve    
def convolve_1D(stim,sta, dt):

    """
    convolves stim with sta
    """

    td = len(sta)

    X = design_matrix_1D(stim, td = td)
  
    response = np.concatenate((np.zeros(1),np.dot(X,sta)))
    
    response_integral = response * dt
    
    return  np.array(response_integral)

