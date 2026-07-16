import odlib
from importlib import reload
import numpy as np
import pandas as pd
reload(odlib)

def main():
    values = pd.read_csv('MahimkarOD5Input.csv')

    i = 3
    #pos, vel = odlib.MoG(2459758.6900936, values['ra1'][i], values['1-Dec'][i], values['sun_x_1'][i], values['sun_y_1'][i], values['sun_z_1'][i], 2459772.6782503, values['ra2'][i], values['2-Dec'][i], values['sun_x_2'][i], values['sun_y_2'][i], values['sun_z_2'][i], 2459774.6955906, values['ra3'][i], values['3-Dec'][i], values['sun_x_3'][i], values['sun_y_3'][i], values['sun_z_3'][i], False, False, False)
    
    #pos, vel = odlib.MoG(values['t1_jd'][i], values['ra1'][i], values['1-Dec'][i], values['sun_x_1'][i], values['sun_y_1'][i], values['sun_z_1'][i], values['t2_jd'][i], values['ra2'][i], values['2-Dec'][i], values['sun_x_2'][i], values['sun_y_2'][i], values['sun_z_2'][i], values['t3_jd'][i], values['ra3'][i], values['3-Dec'][i], values['sun_x_3'][i], values['sun_y_3'][i], values['sun_z_3'][i], True, True, False)
    #print(pos, vel*(2*np.pi/365))


    #Real asteroid with RA and Dec from JPL
    #pos, vel = odlib.MoG(2461208.646013183, '19 27 30.12', '24 05 12.0', 7.759341007743151E-02,  1.012949480246108E+00, -9.086406541867886E-05, 2461220.906437118, '19 16 23.94', '27 53 08.5', -1.294794417652776E-01,  1.008275849695892E+00, -9.158494015923941E-05, 2461222.746091227, '19 14 25.34', '28 20 43.7', -1.602607477542554E-01,  1.003895860852723E+00, -9.607643122211331E-05, True, True, False)

        #Real asteroid with RA and Dec from ours
    #Using degrees
    pos, vel = odlib.MoG(2461208.646013183, 19.45836432, 24.08693997, 7.759341007743151E-02,  1.012949480246108E+00, -9.086406541867886E-05, 2461220.906437118, 19.27329017, 27.88561071, -1.294794417652776E-01,  1.008275849695892E+00, -9.158494015923941E-05, 2461222.746091227, 19.24037683, 28.34537786, -1.602607477542554E-01,  1.003895860852723E+00, -9.607643122211331E-05, False, True, True)

    #Using radians
    #pos, vel = odlib.MoG(2461208.646013183, 5.09418787,0.42039640920568, 7.759341007743151E-02,  1.012949480246108E+00, -9.086406541867886E-05, 2461220.906437118, 5.04573557,0.48669572081769, -1.294794417652776E-01,  1.008275849695892E+00, -9.158494015923941E-05, 2461222.746091227, 5.03711888,0.49472017137768, -1.602607477542554E-01,  1.003895860852723E+00, -9.607643122211331E-05, False, True, False)

    #Using HMS/DMS
    #pos, vel = odlib.MoG(2461208.646013183, '19 27 30.11', '24 05 12.98', 7.759341007743151E-02,  1.012949480246108E+00, -9.086406541867886E-05, 2461220.906437118, '19 16 23.84', 27.88561071, -1.294794417652776E-01,  1.008275849695892E+00, -9.158494015923941E-05, 2461222.746091227, 19.24037683, 28.34537786, -1.602607477542554E-01,  1.003895860852723E+00, -9.607643122211331E-05, False, True, True)

    print(pos, (2*np.pi/365)*vel)


    #odlib.orbital_elements(pos, vel, 1.914529422994113, .1417536798880002, 28.10839246438915, 221.6940522631989, 151.5689338381677, 279.8603654804946, 2461224, 2461220.4064323) 


    #pos, vel = odlib.MoG(values['t1_jd'][i], values['ra1'][i], values['1-Dec'][i], values['sun_x_1'][i], values['sun_y_1'][i], values['sun_z_1'][i], values['t2_jd'][i], values['ra2'][i], values['2-Dec'][i], values['sun_x_2'][i], values['sun_y_2'][i], values['sun_z_2'][i], values['t3_jd'][i], values['ra3'][i], values['3-Dec'][i], values['sun_x_3'][i], values['sun_y_3'][i], values['sun_z_3'][i],values['t_target_jd'][i], True, True)


    #odlib.orbital_elements(pos, vel, values['jpl_a'][i], values['jpl_e'][i], values['jpl_i'][i], values['jpl_loan'][i], values['jpl_aop'][i], values['jpl_ma'][i],  2458301.5)

    #odlib.orbital_elements(pos, vel, 1.5347335844228316, 0.1970533553071983, 11.297804647342733, 196.30886625193716, 142.4976504838525, 322.51152657220473,  2459784.791667, 2459772.6782503)

    




    
