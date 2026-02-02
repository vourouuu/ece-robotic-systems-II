import pyCandle
import numpy as np
import sys
import pandas as pd
import time

tf = 5.              # total time
dt = 0.05            # simulation time step
Ns = 4               # dimension of state
Nc = 2               # dimension of control
S = round(tf/dt) + 1 # number of knot points
print(f"S = {S}")

# Parameters
g = 9.81 # gravity (m/s^2)

# Link 1
l1 = 0.05                   # length (m)
m1 = 0.10548177618443695    # mass (kg)
com1 = 0.05                 # center of mass (m)
I1 = 0.00046166221821039165 # moment of inertia (kg * m^2)
coulomb_fric1 = 0.00305
damp1 = 7.634058385430087e-12

# Link 2
l2 = 0.05                   # length (m)
m2 = 0.07619744360415454    # mass (kg)
com2 = 0.03670036749567022  # center of mass (m)
I2 = 0.00023702395072092597 # moment of inertia (kg * m^2)
coulomb_fric2 = 0.0005106535523065844
damp2 = 0.0007777

# Limits
torque_limit = 0.15

# Cost
Q = np.diag([500., 500., 10., 10.]) 
R = 20. * np.eye(Nc)
QF = 2000. * np.eye(Ns)

# ------------------------- CANdle obj -------------------------
# Create CANdle object and ping FDCAN bus in search of drives. 
# Any found drives will be printed out by the ping() method.
candle = pyCandle.Candle(pyCandle.CAN_BAUD_1M, True)
ids = candle.ping()

if len(ids) == 0: # If no drives found -> quit
    sys.exit("EXIT FALIURE") 

# Add all found to the update list
for id in ids:
    candle.addMd80(id)

# Reset encoder at current position
candle.controlMd80SetEncoderZero(ids[0])      
candle.controlMd80SetEncoderZero(ids[1])      
# Set mode to impedance control
candle.controlMd80Mode(ids[0], pyCandle.RAW_TORQUE)     
candle.controlMd80Mode(ids[1], pyCandle.RAW_TORQUE)     
# Enable the drive
candle.controlMd80Enable(ids[0], True);  
candle.controlMd80Enable(ids[1], True);  
# Set torque limits
candle.md80s[0].setMaxTorque(0.15)
candle.md80s[1].setMaxTorque(0.15)

# --------------------------------------------------------------

# Read gain.csv file 
gains = pd.read_csv('gains.csv')
Ks = gains.values.reshape(-1, 2, 4)

# Read results.csv file 
results = pd.read_csv('results.csv')
q1_bar = results['q1_bar'].values[::2]
q2_bar = results['q2_bar'].values[::2]
q1_dot_bar = results['q1_dot_bar'].values[::2]
q2_dot_bar = results['q2_dot_bar'].values[::2]
u1_bar = results['u1_bar'].values[::2]
u2_bar = results['u2_bar'].values[::2]

xb = np.column_stack((q1_bar, q2_bar, q1_dot_bar, q2_dot_bar))
ub = np.column_stack((u1_bar, u2_bar))

xb = np.array(xb).T 
ub = np.array(ub).T

# CANdle begins
candle.begin()

# Forward Pass: Simulation with Feedback Control
t0 = time.time()
for k in range(S-1):
    q1_actual = candle.md80s[1].getPosition()
    q2_actual = candle.md80s[0].getPosition()
    q1_dot_actual = candle.md80s[1].getVelocity()
    q2_dot_actual = candle.md80s[0].getVelocity()
    x = np.array([[q1_actual],
                  [q2_actual],
                  [q1_dot_actual],
                  [q2_dot_actual]])    
    x_bar = xb[:Ns, k].reshape(Ns,1)

    u_bar = ub[:Nc, k].reshape(Nc,1)
    u = u_bar - Ks[k] @ (x - x_bar)
    u = np.clip(u, -torque_limit, torque_limit)

    candle.md80s[0].setTargetTorque(u[1][0]) # u2
    candle.md80s[1].setTargetTorque(u[0][0]) # u1    
    
    while (time.time() - t0) < dt:
        pass
    t0 += dt

candle.md80s[0].setTargetTorque(0.0)
candle.md80s[1].setTargetTorque(0.0)
time.sleep(0.1)

candle.end()

sys.exit("EXIT SUCCESS")
