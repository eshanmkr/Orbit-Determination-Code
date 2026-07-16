import odlib
from importlib import reload
import numpy as np
import pandas as pd
reload(odlib)

def main():
    values = np.array([19.45836432, 24.08693997, 19.27329017, 27.88561071, 19.24037683, 28.34537786])

    a_arr, e_arr, i_arr, OM_arr, om_arr, M_arr = odlib.monte_carlo(19.45836432, 24.08693997, 19.27329017, 27.88561071, 19.24037683, 28.34537786)

    return(a_arr, e_arr, i_arr, OM_arr, om_arr, M_arr)