#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename   : 3-hardware-implementation.py
Author     : Vrachoriti Alexandra
Date       : 2026-02-04
Description: Real-time TVLQR for trajectory tracking (implementation of the Forward Pass with feddback control)
"""

import pyCandle
import numpy as np
import pandas as pd
import sys
import time

# Initializations
Ns = 4               # dimension of state
Nc = 2               # dimension of control

tf = 5.              # total time
dt = 0.05            # simulation time step
S = round(tf/dt) + 1 # number of knot points

# Parameters
g = 9.81 # gravity (m/s^2)

# [SHOULDER, ELBOW] -> [link 1 (upper), link 2 (lower)]
# SHOULDER
l1 = 0.05                     # length (m)
m1 = 0.10548177618443695      # mass (kg)
com1 = 0.05                   # center of mass (m)
I1 = 0.00046166221821039165   # moment of inertia (kg * m^2)
coulomb_fric1 = 0.00305       # coulomb friction (N)
damp1 = 7.634058385430087e-12 # damping

# ELBOW
l2 = 0.05                     # length (m)
m2 = 0.07619744360415454      # mass (kg)
com2 = 0.03670036749567022    # center of mass (m)
I2 = 0.00023702395072092597   # moment of inertia (kg * m^2)
coulomb_fric2 = 0.0007777     # coulomb friction (N)
damp2 = 0.0005106535523065844 # damping

# Limits
# torque_limit = 0.09
torque_limit = 0.15

# Cost matrices
Q = np.diag([500., 500., 10., 10.]) 
R = 20. * np.eye(Nc)
QF = 2000. * np.eye(Ns)

# CANdle obj
candle = pyCandle.Candle(pyCandle.CAN_BAUD_1M, True)
ids = candle.ping() # motors' ids

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
candle.md80s[0].setMaxTorque(torque_limit)
candle.md80s[1].setMaxTorque(torque_limit)

# Read gain.csv file 
# gains = pd.read_csv('gains-tl-009.csv')
gains = pd.read_csv('gains-tl-015.csv')
Ks = gains.values.reshape(-1, 2, 4)

# Read results.csv file
# results = pd.read_csv('results-tl-009.csv')
results = pd.read_csv('results-tl-015.csv')
q1_bar = results['q1_bar'].values[::2]
q2_bar = results['q2_bar'].values[::2]
q1_dot_bar = results['q1_dot_bar'].values[::2]
q2_dot_bar = results['q2_dot_bar'].values[::2]
u1_bar = results['u1_bar'].values[::2]
u2_bar = results['u2_bar'].values[::2]

xb = np.column_stack((q1_bar, q2_bar, q1_dot_bar, q2_dot_bar))
xb = np.array(xb).T 

ub = np.column_stack((u1_bar, u2_bar))
ub = np.array(ub).T

try:
    # CANdle begins
    candle.begin()

    # Forward Pass with feedback control
    t0 = time.time()
    k = 0
    while True:
        # x_bar, u_bar: nominal trajectory
        x_bar = xb[:Ns, k].reshape(Ns,1)
        u_bar = ub[:Nc, k].reshape(Nc,1)
        
        # Actual state vector: x = [q1, q2, q1_dot, q2_dot]
        q1 = candle.md80s[1].getPosition()
        q2 = candle.md80s[0].getPosition()
        q1_dot = candle.md80s[1].getVelocity()
        q2_dot = candle.md80s[0].getVelocity()
        x = np.array([[q1], [q2], [q1_dot], [q2_dot]])    
        
        # Feedback control: u = u_bar - K (x - x_bar)
        u = u_bar - Ks[k] @ (x - x_bar)
        u = np.clip(u, -torque_limit, torque_limit)

        # Apply torques to the motors
        # > u1 = τ1 = u[0][0] applied to the SHOULDER with (id = 399) or (candle.md80s[1])
        # > u2 = τ2 = u[1][0] applied to the    ELBOW with (id = 375) or (candle.md80s[0])
        candle.md80s[0].setTargetTorque(u[1][0]) # u2
        candle.md80s[1].setTargetTorque(u[0][0]) # u1    
        
        # Active waiting ---> we need real-time loop
        while (time.time() - t0) < dt:
            pass
        
        # Holds the double pendulum in the upright vertical position
        if(k < S-2):
            k = k + 1
        else: # If the double pendulum is disturbed, then we must return it to its upright vertical position 
            # Calculate all angular distances between current angles (q1, q2) and all nominal angles (q1_bar, q2_bar)
            q_diff = np.arctan2(np.sin(xb[:2, :] - x[:2]), np.cos(xb[:2, :] - x[:2]))
            
            # Minimum angular distance
            min_dist = np.linalg.norm(q_diff, axis=0)
            
            idx = np.argmin(min_dist)
            k = min(idx, S-2) # for safety, cause kE[0, S-2]
        
        t0 += dt         
except KeyboardInterrupt:
    print("\n---> Safety button pressed!")

    candle.md80s[0].setTargetTorque(0)
    candle.md80s[1].setTargetTorque(0)
    time.sleep(0.1)

    sys.exit("EXIT SUCCESS")