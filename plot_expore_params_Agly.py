from BA1A2_Model import BA1A2_Model
from filter import filter_alpha_norm
from convolutions import convolve_1D
from dynamical_systems import IPL_rectified, IPL_rectified_occupancy, IPL_rectified_occupancy_nV,IPL_occupancy,IPL
from nonlinearities import N
from utils import  make_param_dict, save_dict,save_fig,make_directory
from stimuli import impulse_stimulus, step_stimulus
from load_data import get_euler_stimulus
from simulate import simulate_OSR
from matplotlib.backends import backend_pdf
from matplotlib import pyplot as plt
import os
import numpy as np
import json
import pandas as pd
import seaborn as sns



filepath = "/user/sebert/home/Documents/Simulations/osr_model/explore_Agly_params"

df = pd.read_csv(f'{filepath}/DataFrame_Agly_params_slope_effect.csv')

# plot heatmap for beta
df_tauA1_wA1_delay = df.pivot('w_A1','tau_A1','delay')
df_tauA1_wA1_slope = df.pivot('w_A1','tau_A1','slope')


# print best params
print('params for maximal slope')
print(df.iloc[df['slope'].idxmax()])

fig, ax = plt.subplots(1,2)

sns.heatmap(df_tauA1_wA1_delay, ax = ax[0])
sns.heatmap(df_tauA1_wA1_slope, ax = ax[1])


ax[0].set_title('Latency for 16 Hz')
ax[1].set_title('Slope')


plt.show()


fig, ax = plt.subplots(1,2)

df_ = df.query('tau_A1 == 0.23 and slope >= -0.5 and slope <= 2')

df_.plot.scatter(x = 'w_A1', y = 'slope', ax = ax[0])
df_.plot.scatter(x = 'w_A1', y = 'delay', ax = ax[1])

ax[0].set_title('Slope')
ax[1].set_title('Latency 16 Hz')


plt.show()



# save the plots

save_fig(f'{filepath}/heatmaps_tau_A1_w_A1.png',fig)


