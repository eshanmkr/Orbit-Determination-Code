import odlib
from importlib import reload
import numpy as np
reload(odlib)

def main():
    values = np.loadtxt('MahimkarOD2Input.txt')
    odlib.orbital_elements(values[0], (365.256898/(2*np.pi))*values[1], float(values[2,0]), float(values[2,1]), float(values[2,2]), float(values[3,0]), float(values[3,1]), float(values[3,2]), 2458313.500000000)