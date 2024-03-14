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



filepath = "/user/sebert/home/Documents/Simulations/osr_model/explore_occupancy_params/params_exploration_occupancy"

df = pd.read_csv(f'{filepath}/DataFrame_occupancy_params_slope_effect.csv')
df['beta'] = df['beta'].round(decimals =2)

# plot heatmap for beta
df_beta_n_num = df.pivot('k_ratio','beta','n_diff')
df_beta_n_an = df.pivot('k_ratio','beta','n_diff_calc')
df_beta_slope = df.pivot('k_ratio','beta','slope')


# print best params
print('params for maximal slope')
print(df.iloc[df['slope'].idxmax()])


fig, ax = plt.subplots(1,3)

sns.heatmap(df_beta_n_an, ax = ax[0])
sns.heatmap(df_beta_n_num, ax = ax[1])
sns.heatmap(df_beta_slope, ax = ax[2])

ax[1].set_title('Difference in n_max from simulations')
ax[0].set_title('Difference in n_max calculated')
ax[2].set_title('Slope')


plt.show()
# plo occupancy time constant


fig2, ax = plt.subplots(1,3)

df.plot.scatter(x= 'tau_n', y = 'n_diff_calc', ax = ax[0])
df.plot.scatter(x= 'tau_n', y = 'n_diff', ax = ax[1])
df.plot.scatter(x= 'tau_n', y = 'slope', ax = ax[2])

ax[1].set_title('Difference in n_max from simulations')
ax[0].set_title('Difference in n_max calculated')
ax[2].set_title('Slope')


plt.show()

# save the plots

save_fig(f'{filepath}/heatmaps_k_ratio_beta.png',fig)
save_fig(f'{filepath}/tau_n.png',fig2)



