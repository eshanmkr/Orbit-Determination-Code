import odlib
from importlib import reload
import numpy as np
reload(odlib)

def main():
    values = np.loadtxt('MahimkarOD3Input.txt')
    
    odlib.ephemeris(float(values[2,0]), float(values[2,1]), float(values[2,2]), float(values[3,0]), float(values[3,1]), float(values[3,2]), 2458313.5, 2458314.5, values[4], 273.05783, 36.05675)