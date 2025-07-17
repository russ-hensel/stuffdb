#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  6 14:01:49 2025

@author: russ
"""


# ---- tof

# ---- imports

# ---- end imports


#-------------------------------






# ---- eof


# %% Cell 1: Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %% Cell 2: Load data
data = pd.read_csv('my_data.csv')
print(data.head())

# %% Cell 3: Data analysis
mean_value = data['column'].mean()
print(f"Mean: {mean_value}")

# %%% Cell 4: Plotting
plt.figure(figsize=(10, 6))
plt.plot(data['x'], data['y'])
plt.title('My Plot')
plt.show()