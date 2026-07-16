#I had to remove all of the headers so it might have been easier to use Pandas
import numpy as np
import matplotlib.pyplot as plt

#This is the function
def find_h():
    #This imports the file
    values = np.loadtxt('MahimkarOD1Input.txt')
    #This does the math. This line converts the cross product to gaussian days as well.
    h = (365.2568983/(2*np.pi))*(np.cross(values[0], values[1]))
    return h



def a(pos, vel):
    v_sqr = np.sum(vel**2)
    r = (np.sum(pos**2))**0.5
    return "a", 1/((2/r)-(v_sqr))

def e(pos, vel):
    h = np.cross(pos, vel)
    #print("hs" +str(h))
    h = (np.sum(h**2))**0.5
    #print(h)
    
    name, value = a(pos, vel)
    return "e", ((1-((h**2)/value))**0.5)


def i(pos, vel):
    h = np.cross(pos, vel)
    hz = h[2]
    h = (np.sum(h**2))**0.5
    return "i", np.rad2deg(np.arccos(hz/h))


def cap_omega(pos, vel):
    h = np.cross(pos, vel)
    hx = h[0]
    hy = h[1]
    h = (np.sum(h**2))**0.5
    name, value = i(pos,vel)
    value = np.deg2rad(value)
    sin_om = hx/(h*np.sin(value))
    cos_om = -1*hy/(h*np.sin(value))
    return "Capital Omega", np.rad2deg(quadrant_checker(cos_om, sin_om))
    


def omega(pos, vel):
    x = pos[0]
    y = pos[1]
    z = pos[2]
    h = np.cross(pos, vel)
    h = (np.sum(h**2))**0.5
    name, value = cap_omega(pos,vel)
    r = (np.sum(pos**2))**0.5
    value = np.deg2rad(value)
    name1, value1 = i(pos,vel)
    value1 = np.deg2rad(value1)
    sin_U = z/(r*np.sin(value1))
    cos_U = ((x*np.cos(value))+(y*np.sin(value)))/r
    U = (quadrant_checker(cos_U, sin_U))
    name2, value2 = e(pos, vel)
    name3, value3 = a(pos, vel)
    
    cos_anom = (1/value2)*(((value3*(1-value2**2))/r)-1)
    sin_anom = (value3*(1-value2**2))/(h*value2)*((np.dot(pos, vel))/r)
    anom = (quadrant_checker(cos_anom, sin_anom))
    return "omega", np.rad2deg((U - anom)%(2*np.pi))

    
def E(pos, vel):
    r = (np.sum(pos**2))**0.5
    h = np.cross(pos, vel)
    h = (np.sum(h**2))**0.5
    
    name2, value2 = e(pos, vel)
    name3, value3 = a(pos, vel)
    

    cos_anom = (1/value2)*(((value3*(1-value2**2))/r)-1)
    sin_anom = (value3*(1-value2**2))/(h*value2)*((np.dot(pos, vel))/r)
    anom = (quadrant_checker(cos_anom, sin_anom))

    b = ((value3**2)*(1-value2**2))**0.5
    cos_E = (value2) + (r*np.cos(anom))/value3
    sin_E = (r*np.sin(anom))/b
    
    E = quadrant_checker(cos_E, sin_E)

    return E
    

def M(pos, vel):
    ecc_anom = E(pos, vel)
    name, e1 = e(pos, vel)
    M = ecc_anom - e1*(np.sin(ecc_anom))
    return float(np.rad2deg(M))
    


def quadrant_checker(cos, sin):
    if np.sign(sin)==1 and np.sign(cos)==1:
        quadrant = 1
    elif np.sign(sin)==1 and np.sign(cos)==-1:
        quadrant = 2
    elif np.sign(sin)==-1 and np.sign(cos)==-1:
        quadrant = 3
    elif np.sign(sin)==-1 and np.sign(cos)==1:
        quadrant = 4

    angle = np.arcsin(sin)
    if quadrant == 2 or quadrant == 3:
        return (np.pi - angle)
    elif quadrant == 4:
        return((2*np.pi)+angle)
    else:
        return angle
        
def orbital_elements(pos, vel, ref_a, ref_e, ref_i, ref_cap_om, ref_om, ref_M,  JD_predict, JD_current):
    print('pos,vel')
    print(pos,vel)
    name_a, a1 = a(pos, vel)
    name_e, e1 = e(pos, vel)
    name_i, i1 = i(pos, vel)
    name_cap_om, cap_om = cap_omega(pos, vel)
    name_om, om = omega(pos, vel)

    n = 1/(a1**1.5)
    M1 = M(pos, vel)
    M_dif = ( JD_predict - JD_current)*((2*np.pi)/365.2568983)
    M_dif = np.rad2deg(M_dif)
    M_new = n*M_dif + M1

    percent_a = (abs(ref_a - a1))/((ref_a))*100
    percent_e = (abs(ref_e - e1))/((ref_e))*100
    percent_i = (abs(ref_i - i1))/((ref_i))*100
    percent_cap_om = (abs(ref_cap_om - cap_om))/((ref_cap_om))*100
    percent_om = (abs(ref_om - om))/((ref_om))*100
    percent_M = (abs(ref_M - M_new))/((ref_M))*100

    print("Orbital Element: "+str(name_a)+" "+"reference value:"+str(ref_a)+" "+"calculated value:"+str(a1)+" "+"percent difference:"+str(percent_a))
    print("Orbital Element: "+str(name_e)+" "+"reference value:"+str(ref_e)+" "+"calculated value:"+str(e1)+" "+"percent difference:"+str(percent_e))
    print("Orbital Element: "+str(name_i)+" "+"reference value:"+str(ref_i)+" "+"calculated value:"+str(i1)+" "+"percent difference:"+str(percent_i))
    print("Orbital Element: "+str(name_cap_om)+" "+"reference value:"+str(ref_cap_om)+" "+"calculated value:"+str(cap_om)+" "+"percent difference:"+str(percent_cap_om))
    print("Orbital Element: "+str(name_om)+" "+"reference value:"+str(ref_om)+" "+"calculated value:"+str(om)+" "+"percent difference:"+str(percent_om))
    print("Orbital Element: M"+" "+"reference value:"+str(ref_M)+" "+"calculated value:"+str(M_new)+" "+"percent difference:"+str(percent_M))
    print("Julian Date: "+str(JD_predict))

    #return(float(a), float(e), float(i) , float(cap_om) float(om), float(M))
    


def error(calc, actual):
    err = ((abs(calc-actual))/actual)*100
    return err

    
def NR(e, M):
    dif = 1000
    guess = M
    repet = 0
    while dif > 0.00001:
        func = guess - (e*(np.sin(guess))) - M
        dfunc = 1 - (e*np.cos(guess))
        old_guess = guess
        guess = guess - (func/dfunc)
        dif = abs(guess-old_guess)
    return guess
    

def ephemeris(a, e, i, cap_om, om, M, JD_predict, JD_current, sun_earth_vector, ref_RA, ref_Dec):
    #Find M
    n = 1/(a**1.5)
    M = np.deg2rad(M)
    M_dif = (JD_current - JD_predict)*((2*np.pi)/365.2568983)
    M_new = n*M_dif + M
    E = NR(e, M_new)

    #print(M_new)

    i = np.deg2rad(i)
    cap_om = np.deg2rad(cap_om)
    om = np.deg2rad(om)
            
    

    #Find r
    r = np.array([[(a*np.cos(E))-(a*e)], 
                  [(a*np.sqrt(1-e**2))*np.sin(E)], 
                  [0]])



    #Rotation Matrices
    rot1 = np.array([[np.cos(om), -np.sin(om), 0],
                    [np.sin(om), np.cos(om), 0],
                    [0,0,1]])
    r_rot1 = rot1 @ r


    rot2 = np.array([[1,0,0],
                     [0, np.cos(i), -np.sin(i)],
                     [0, np.sin(i), np.cos(i)]])
    r_rot2 = rot2 @ r_rot1

    rot3 = np.array([[np.cos(cap_om), -np.sin(cap_om), 0],
                    [np.sin(cap_om), np.cos(cap_om), 0],
                    [0,0,1]])
    r_rot3 = rot3 @ r_rot2

    obliq = 23.5

    obliq = np.deg2rad(obliq)

    rot4 = np.array([[1,0,0],
                     [0, np.cos(obliq), -np.sin(obliq)],
                     [0, np.sin(obliq), np.cos(obliq)]])
    r_rot4 = rot4 @ r_rot3


    #Rotate the sun earth vector
    rot5 = np.array([[1,0,0],
                     [0, np.cos(obliq), -np.sin(obliq)],
                     [0, np.sin(obliq), np.cos(obliq)]])
    sun_earth_vector = sun_earth_vector.reshape(-1,1)
    rot_earth_sun = rot5 @ sun_earth_vector

    #Make ro
    ro = r_rot4 + rot_earth_sun
    ro_hat = ro/(np.sqrt(np.sum(ro**2)))


    #Find dec and RA
    dec = np.arcsin(ro_hat[2,0])

    cos_RA = ro_hat[0,0]/(np.cos(dec))
    sin_RA = ro_hat[1,0]/(np.cos(dec))

    
    RA = quadrant_checker(cos_RA, sin_RA)
    dec = np.rad2deg(dec)
    RA = np.rad2deg(RA)

    print("RA: ", str(RA))
    print("Dec: ", str(dec))

    RA_error = error(RA, ref_RA)
    Dec_error = error(dec, ref_Dec)

    print("RA: " + str(RA) + "; expected value: " + str(ref_RA) + "; percent error: " + str(RA_error)) 
    print("Dec: " + str(dec) + "; expected value: " + str(ref_Dec) + "; percent error: " + str(Dec_error)) 



def f_mog(x,y,z,vx,vy,vz, tao, tag, f_out, g_out):
    #This turns the inputs into vectors
    pos = np.array([x,y,z])
    vel = np.array([vx,vy,vz])
    posm = np.sqrt(np.sum(pos**2))
    f = 0

    if tag==True:
        #Fourth degree f
        f = 1-((tao**2)/(2*(posm**3)))+(((np.dot(pos, vel))*(tao**3))/(2*(posm**5)))+(((tao**4)/(24*(posm**3)))*((3*(((np.dot(vel,vel))/(posm**2))-(1/(posm**3))))-(15*(((np.dot(pos, vel))/(posm**2))**2))+(1/(posm**3))))
    else:
        #Thrid degree f
        f = 1-(((1)*(tao**2))/(2*(posm**3)))+(((np.dot(pos, vel))/(2*(posm**5)))*(tao**3))

    #This is the percent error
    #error = abs(((f-f_out))/(f_out))*100

    #return("Calculated f: " + str(f) + ". Percent error: " + str(error))
    return f

    

def g_mog(x,y,z,vx,vy,vz,tao, tag, f_out, g_out):
    #This turns the inputs into vectors
    pos = np.array([x,y,z])
    vel = np.array([vx,vy,vz])
    posm = np.sqrt(np.sum(pos**2))
    g = 0
    
    if tag==True:
        #Fourth degree g
        g = tao-((tao**3)/(6*(posm**3)))+(((np.dot(pos,vel))/(4*(posm**5)))*(tao**4))
    else:
        #Third degree g
        g = tao-((1*(tao**3))/(6*(posm**3)))

    #error = abs(((g-g_out))/(g_out))*100

    #return("Calculated g: " + str(g) + ". Percent error: " + str(error))
    return g

def hms_to_deg(hms):
    # Converts an angle in (hours, minutes, seconds) to decimal degrees
    decimalDeg = (float(hms[0])*15) + (float(hms[1])*0.25) + (float(hms[2]) *(0.25/60))
    radDeg = np.deg2rad(decimalDeg)
    return (radDeg)

def dms_to_deg(dms):
    decimalDeg = (float(dms[0])) + (float(dms[1])/60) + (float(dms[2])/3600)
    
    if float(dms[0]) < 0:
        return -np.deg2rad(decimalDeg)

    else:
        return np.deg2rad(decimalDeg)

                           
    
    

def MoG(t1, RA1, Dec1, sun_x1, sun_y1, sun_z1, t2, RA2, Dec2, sun_x2, sun_y2, sun_z2, t3, RA3, Dec3, sun_x3, sun_y3, sun_z3, HMS, rot_sun, deg2rad):


    k = (2*np.pi)/(365.2568983)
    change = 100
    counter = 0
  
    if HMS==True:
        RA1 = hms_to_deg(str(RA1).split(" "))
        RA2 = hms_to_deg(str(RA2).split(" "))
        RA3 = hms_to_deg(str(RA3).split(" "))

        Dec1 = dms_to_deg(str(Dec1).split(" "))
        Dec2 = dms_to_deg(str(Dec2).split(" "))
        Dec3 = dms_to_deg(str(Dec3).split(" "))

    if deg2rad == True:
        RA1 = RA1 * (np.pi/12)
        RA2 = RA2 * (np.pi/12)
        RA3 = RA3 * (np.pi/12)

        Dec1 = np.deg2rad(Dec1)
        Dec2 = np.deg2rad(Dec2)
        Dec3 = np.deg2rad(Dec3)
    

    #Make Tau
    tau0 = (k*(t3-t1))
    tau1 = (k*(t1-t2))
    tau3 = (k*(t3-t2))

    #Make ro1

    #print(RA1, RA2, RA3)
    #print(Dec1, Dec2, Dec3)


    

    
    
    ro1 = np.array([(np.cos(float(RA1)))*(np.cos(float(Dec1))), (np.sin(float(RA1)))*(np.cos(float(Dec1))), np.sin(float(Dec1))])

    ro2 = np.array([(np.cos(float(RA2)))*(np.cos(float(Dec2))), (np.sin(float(RA2)))*(np.cos(float(Dec2))), np.sin(float(Dec2))])

    ro3 = np.array([(np.cos(float(RA3)))*(np.cos(float(Dec3))), (np.sin(float(RA3)))*(np.cos(float(Dec3))), np.sin(float(Dec3))])

    #print(ro1, ro2, ro3)


    #Make Sun Vectors
    R1 = np.array([sun_x1,
                  sun_y1,
                   sun_z1])
    R2 = np.array([sun_x2,
                  sun_y2,
                   sun_z2])
    R3 = np.array([sun_x3,
                  sun_y3,
                   sun_z3])

    #print(R1, R2, R3)
    
    #Rotate the sun vectors if necessary

    obliq = np.deg2rad(23.4374)
    
    rotR_clock = np.array([[1,0,0],
                     [0, np.cos(obliq), -np.sin(obliq)],
                     [0, np.sin(obliq), np.cos(obliq)]])
    if rot_sun==True:
        
        R1 = R1.reshape(-1,1)
        R2 = R2.reshape(-1,1)
        R3 = R3.reshape(-1,1)
        
        R1 = rotR_clock @ R1
        R2 = rotR_clock @ R2
        R3 = rotR_clock @ R3

        R1 = R1.flatten()
        R2 = R2.flatten()
        R3 = R3.flatten()


    #print(rotR) 
    

    #ro1 = rotR @ ro1
    #ro2 = rotR @ ro2
    #ro3 = rotR @ ro3
    

    #R1 = R1.flatten()
    #R2 = R2.flatten()
    #R3 = R3.flatten()

    #ro1 = ro1.flatten()
    #ro2 = ro2.flatten()
    #ro3 = ro3.flatten()


    #print(R1)
    #print(R2)
    #print(R3)


    #Do the determinants
    D0 = np.dot(ro1, (np.cross(ro2, ro3)))
    D11 = np.dot(ro3, (np.cross(R1, ro2)))
    D12 = np.dot(ro3, (np.cross(R2, ro2)))
    D13 = np.dot(ro3, (np.cross(R3, ro2)))
    D21 = np.dot(ro3, (np.cross(ro1, R1)))
    D22 = np.dot(ro3, (np.cross(ro1, R2)))
    D23 = np.dot(ro3, (np.cross(ro1, R3)))
    D31 = np.dot(ro1, (np.cross(ro2, R1)))
    D32 = np.dot(ro1, (np.cross(ro2, R2)))
    D33 = np.dot(ro1, (np.cross(ro2, R3)))

    #print(D0, D11, D12, D13, D21, D22, D23, D31, D32, D33)


    a1 = (t3-t2)/(t3-t1)
    a3 = (t2-t1)/(t3-t1)

    # print("sam wuz here", D0, D11, D12, D13, D21, D22, D23, D31, D32, D33)

    i = 0
    
    #This is the iteration loop
    while change > (10**-15):
        
        counter+=1
        #Make the magnitude of the ro
        mag_ro1 = ((a1*D11)-(D12)+(a3*D13))/(a1*D0)
        mag_ro2 = ((a1*D21)-(D22)+(a3*D23))/((-1)*D0)
        mag_ro3 = ((a1*D31)-(D32)+(a3*D33))/(a3*D0)

       
        #print("mag_ros")
        #print(mag_ro1)
        #print(mag_ro2)
        #print(mag_ro3)
        
        #Make the r vectors
        rho1 = mag_ro1*ro1
        rho2 = mag_ro2*ro2
        rho3 = mag_ro3*ro3
        
        r1 = rho1-R1
        r2 = rho2-R2
        r3 = rho3-R3

        

        #print(r1, r2, r3)

        
        #print("r1")
        #print(r1)
        #print("r2")
        #print(r2)
        #print("r3")
        #print(r3)

        
        
        if i==0:
            #Estimate the velocity vectors on the first iteration through the loop
            v12 = (r2-r1)/(t2-t1)
            v23 = (r3-r2)/(t3-t2) # t3 - t2
            
            #print("v12 and v23")
            #print(v12)
            #print(v23)
            
            v2 = (((t3-t2)*v12)+((t2-t1)*v23))/(t3-t1)

        #print("v2")
        #print(v2)

        #Create the vector components
        r2x = r2[0]
        r2y = r2[1]
        r2z = r2[2]

        v2x = v2[0]
        v2y = v2[1]
        v2z = v2[2]

        t1_act = t1 - (mag_ro1/173.144643267)
        t2_act = t2 - (mag_ro2/173.144643267)
        t3_act = t3 - (mag_ro3/173.144643267)

        tau0 = (k*(t3_act-t1_act))
        tau1 = (k*(t1_act-t2_act))
        tau3 = (k*(t3_act-t2_act))

        
        #Find f and g for night 1 and night 3
        f1 = f_mog(r2x,r2y,r2z,v2x,v2y,v2z, tau1, True, 0, 0)

        f3 = f_mog(r2x,r2y,r2z,v2x,v2y,v2z, tau3, True, 0, 0)

        g1 = g_mog(r2x,r2y,r2z,v2x,v2y,v2z, tau1, True, 0, 0)

        g3 = g_mog(r2x,r2y,r2z,v2x,v2y,v2z, tau3, True, 0, 0)

        #print("f's and g's")
        #print(f1, f3)
        #print(g1, g3)

        
        #Calculate a1 and a3
        r2 = (g3 *r1 - g1 *r3)/(f1 * g3 - g1 * f3)
        v2 = (f3 * r1 - f1 * r3)/(f3 * g1 - f1 *g3)
        
        a1 = g3/((f1*g3)-(g1*f3))
        a3 = (-g1)/((f1*g3)-(g1*f3))

        #print("a1's and a3's")
       # print(a1, a3)

        
        #If its NOT in the first iteration, calculate the change
        if i != 0:
            change = abs((np.linalg.norm(r2) - np.linalg.norm(r2_old))/(np.linalg.norm(r2)))

        r2_old = r2


        if i==10000:
            break 

        #Increase i and create and counter
        
        i+=1

        
    #print("final v2 before rot")
    #print(v2)
    
    r2 = r2.reshape(-1,1)
    v2 = v2.reshape(-1,1)

    #print(v2)

    
    obliq = np.deg2rad(23.4374)

    rotX = np.array([[1,0,0],
                    [0, np.cos(obliq), np.sin(obliq)],
                    [0, -np.sin(obliq), np.cos(obliq)]])

    v2 =  rotX @ (v2)

    r2 = rotX @ r2
    #print('v2!', v2)
    
    r2 = r2.flatten()
    v2 = v2.flatten()

    #print(counter)

    v2 = v2

    return (r2, v2)


def monte_carlo(RA1, Dec1, RA2, Dec2, RA3, Dec3):

    a_arr= np.array([])
    e_arr = np.array([])
    i_arr= np.array([])
    OM_arr = np.array([])
    om_arr= np.array([])
    M_arr = np.array([])

    times = 100000

    for j in range (times):
            RA1_rands = np.random.normal(loc=RA1, scale=4.465379325886591e-06)
            Dec1_rands = np.random.normal(loc=Dec1, scale=5.975405854182289e-05) 

            RA2_rands = np.random.normal(loc=RA2, scale=1.8711761174394722e-05)
            Dec2_rands = np.random.normal(loc=Dec2, scale=0.000497835905623512)

            RA3_rands = np.random.normal(loc=RA3, scale=8.894763915472132e-07)
            Dec3_rands = np.random.normal(loc=Dec3, scale=8.103180336710872e-05)
            
            pos, vel = MoG(2461208.646013183, RA1_rands, Dec1_rands, 7.759341007743151E-02,  1.012949480246108E+00, -9.086406541867886E-05, 2461220.906437118, RA2_rands, Dec2_rands, -1.294794417652776E-01,  1.008275849695892E+00, -9.158494015923941E-05, 2461222.746091227, RA3_rands, Dec3_rands, -1.602607477542554E-01,  1.003895860852723E+00, -9.607643122211331E-05, False, True, True)

            name_a, value_a = a(pos,vel)
            name_e, value_e = e(pos,vel)
            name_i, value_i = i(pos,vel)
            name_OM, value_OM = cap_omega(pos,vel)
            name_om, value_om = omega(pos,vel)
            value_M = M(pos,vel)

            a_arr = np.append(a_arr, value_a)
            e_arr = np.append(e_arr, value_e)
            i_arr = np.append(i_arr, value_i)
            OM_arr = np.append(OM_arr, value_OM)
            om_arr = np.append(om_arr, value_om)
            M_arr = np.append(M_arr, value_M)
    '''
    a_calc = np.mean(a_arr)
    print("Mean of a: " + str(a_calc))
    stdev_a = np.std(a_arr)
    percent_error_a = (abs((a_calc-1.914529422994113))/(1.914529422994113))*100
    print("Percent error of a: "+ str(percent_error_a))
    print("Standard deviation of a: " + str(stdev_a))
    sdom_a = stdev_a/((times)**0.5)
    print("Standard deviation of the mean for a: " + str(sdom_a))

    e_calc = np.mean(e_arr)
    print("Mean of e: " + str(e_calc))
    stdev_e = np.std(e_arr)
    percent_error_e = (abs((e_calc-0.1417536798880002))/(0.1417536798880002))*100
    print("Percent error of e: "+ str(percent_error_e))
    print("Standard deviation of e: " + str(stdev_e))
    sdom_e = stdev_e/((times)**0.5)
    print("Standard deviation of the mean for e: " + str(sdom_e))

    i_calc = np.mean(i_arr)
    print("Mean of i: " + str(i_calc))
    stdev_i = np.std(i_arr)
    percent_error_i = (abs((i_calc-28.10839246438915))/(28.10839246438915))*100
    print("Percent error of i: "+ str(percent_error_i))
    print("Standard deviation of i: " + str(stdev_i))
    sdom_i = stdev_i/((times)**0.5)
    print("Standard deviation of the mean for i: " + str(sdom_i))

    OM_calc = np.mean(OM_arr)
    print("Mean of OM: " + str(OM_calc))
    stdev_OM = np.std(OM_arr)
    percent_error_OM = (abs((OM_calc-221.6940522631989))/(221.6940522631989))*100
    print("Percent error of OM: "+ str(percent_error_OM))
    print("Standard deviation of OM: " + str(stdev_OM))
    sdom_OM = stdev_OM/((times)**0.5)
    print("Standard deviation of the mean for OM: " + str(sdom_OM))

    om_calc = np.mean(om_arr)
    print("Mean of om: " + str(om_calc))
    stdev_om = np.std(om_arr)
    percent_error_om = (abs((om_calc-151.5689338381677))/(151.5689338381677))*100
    print("Percent error of om: "+ str(percent_error_om))
    print("Standard deviation of om: " + str(stdev_om))
    sdom_om = stdev_om/((times)**0.5)
    print("Standard deviation of the mean for OM: " + str(sdom_OM))


    M_calc = np.mean(M_arr)
    print("Mean of M: " + str(M_calc))
    stdev_M = np.std(M_arr)
    percent_error_M = (abs((M_calc-279.8603654804946))/(279.8603654804946))*100
    print("Percent error of M: "+ str(percent_error_M))
    print("Standard deviation of M: " + str(stdev_M))
    sdom_M = stdev_M/((times)**0.5)
    print("Standard deviation of the mean for M: " + str(sdom_M))

    
    bin_count = 50
    #Semi major plot

    bins = np.linspace(1.8, 2.1, bin_count+1)

    jennifer_a= 1.914529422994113

    plt.hist(a_arr, bins, color='blue', alpha=0.5, label='Semi-major')
    plt.axvline(jennifer_a, color='orange', label='JPL Value')
    plt.axvline(a_calc, color='black', label='Mean Value')
    plt.legend()
    plt.xlabel('Semi-major Axis')
    plt.ylabel('Counts')
    plt.title('Distribution of the Semi-Major Axis for RA and Dec Uncertainties')
    plt.show()


#Eccentricity plot

    

    bins = np.linspace(0.05, 0.2, bin_count+1)

    jennifer_e= 0.1417536798880002

    plt.hist(e_arr, bins, color='blue', alpha=0.5, label='Eccentricity')
    plt.axvline(jennifer_e, color='orange', label='JPL value')
    plt.axvline(e_calc, color='black', label='Mean Value')
    plt.legend()
    plt.xlabel('Eccentricity')
    plt.ylabel('Counts')
    plt.title('Distribution of the Eccentricity for RA and Dec Uncertainties')
    plt.show()

#Inclination plot

    bins = np.linspace(25, 32.5, bin_count+1)

    jennifer_i= 28.10839246438915

    plt.hist(i_arr, bins, color='blue', alpha=0.5, label='Eccentricity')
    plt.axvline(jennifer_i, color='orange', label='JPL value')
    plt.axvline(i_calc, color='black', label='Mean Value')
    plt.legend()
    plt.xlabel('Inclination')
    plt.ylabel('Counts')
    plt.title('Distribution of the Inclination for RA and Dec Uncertainties')
    plt.show()


#OMEGA plot

    bins = np.linspace(216, 228, bin_count+1)

    jennifer_OM= 221.6940522631989

    plt.hist(OM_arr, bins, color='blue', alpha=0.5, label='LOAN')
    plt.axvline(jennifer_OM, color='orange', label='JPL value')
    plt.axvline(OM_calc, color='black', label='Mean Value')
    plt.legend()
    plt.xlabel('Longitude of the Ascending Node')
    plt.ylabel('Counts')
    plt.title('Distribution of the Longitude of the Ascending Node for RA and Dec Uncertainties')
    plt.show()


#omega plot

    bins = np.linspace(120, 170, bin_count+1)

    jennifer_om = 151.5689338381677

    plt.hist(om_arr, bins, color='blue', alpha=0.5, label='AOP')
    plt.axvline(jennifer_om, color='orange', label='JPL value')
    plt.axvline(om_calc, color='black', label='Mean Value')
    plt.legend()
    plt.xlabel('Argument of the Perihelion')
    plt.ylabel('Counts')
    plt.title('Distribution of the Argument of the Perihelion for RA and Dec Uncertainties')
    plt.show()


#Mean anomaly plot

    bins = np.linspace(280, 315, bin_count+1)

    jennifer_M = 279.8603654804946

    plt.hist(M_arr, bins, color='blue', alpha=0.5, label='M')
    plt.axvline(jennifer_M, color='orange', label='JPL value')
    plt.axvline(M_calc, color='black', label='Mean Value')
    plt.legend()
    plt.xlabel('Mean Anomaly')
    plt.ylabel('Counts')
    plt.title('Distribution of the Mean Anomaly for RA and Dec Uncertainties')
    plt.show()
    '''

    return (a_arr, e_arr, i_arr, OM_arr, om_arr, M_arr)


    



                


    



    

    


    

    
            

            

            
            
            
        
        
    



        
            
            
            

    

    




























































              


    



    




    
    
    
    































    

    
        
    



