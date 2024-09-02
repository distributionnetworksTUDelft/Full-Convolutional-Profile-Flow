import os
import sys
_parent_path =os.path.join(os.path.dirname(__file__), '..','..')
sys.path.append(_parent_path)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import tools.evaluation_m as em

font_path = 'tools/TIMES.TTF'
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
front_size = 17

# read the data
data_path = os.path.join(_parent_path, 'data/nl_data_1household.csv')
np_array = pd.read_csv(data_path).iloc[:,3:].values
np_array = np_array[~pd.isna(np_array).any(axis=1)]
split_ratio = 0.8


_lenggth_test = np_array.shape[0] - int(np_array.shape[0] * split_ratio)
test_data = np_array[-_lenggth_test:,:]

mmd_s = []
for _s_r in range(1, 11, 1):
    amount_train_data = 0.6*_s_r/10 
    _length_train = int(np_array.shape[0] * split_ratio * amount_train_data)
    train_data = np_array[:_length_train,:]
    _mmd = em.MMD_kernel(train_data, test_data)
    mmd_s.append(_mmd)

# read train data
path = 'exp/data_requirement_ana/data_requirement_ana.csv'
train_data_mm = pd.read_csv(path,sep=';')
mm_min_100 = train_data_mm['100 - MMD'].min()
mm_min_60 = train_data_mm['60 - MMD'].min()
mm_min_30 = train_data_mm['30 - MMD'].min()
mm_min_10 = train_data_mm['10 - MMD'].min()
mmd_train_data = [mm_min_100, mm_min_60, mm_min_30, mm_min_10]
mmd_train_data_indx = [100/100, 60/100, 30/100, 10/100]
x_axis = np.linspace(0, 1, 10)
# plot the mmd
plt.figure()
plt.plot(x_axis, mmd_s, label='MMD between training and test data')
plt.scatter(mmd_train_data_indx, mmd_train_data, label='MMD between generated and test data', c='orange')
plt.plot(mmd_train_data_indx, mmd_train_data, linestyle='--')
plt.xlabel('Percentage of training data [-]', fontsize=front_size, fontproperties=font_prop)
plt.ylabel('MMD [-]', fontsize=front_size, fontproperties=font_prop)
plt.legend(fontsize=front_size, prop=font_prop)
plt.savefig('exp/data_requirement_ana/data_requirement_ana.png')