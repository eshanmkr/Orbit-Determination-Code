import odlib
from importlib import reload
import numpy as np
import pandas as pd
reload(odlib)

def main():
    values = pd.read_csv('MahimkarOD4Input.csv')

    for i in range (6):
        print(odlib.f_mog(values['r2_x'][i], values['r2_y'][i], values['r2_z'][i], values['v2_x'][i], values['v2_y'][i], values['v2_z'][i], values['tau'][i], values['order4'][i], values['f_output'][i], values['g_output'][i]))
              
        print(odlib.g_mog(values['r2_x'][i], values['r2_y'][i], values['r2_z'][i], values['v2_x'][i], values['v2_y'][i], values['v2_z'][i], values['tau'][i], values['order4'][i], values['f_output'][i], values['g_output'][i]))
        

