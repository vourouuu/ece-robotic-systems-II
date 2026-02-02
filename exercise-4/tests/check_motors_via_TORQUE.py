import pyCandle
import sys
import time

# Create CANdle object and ping FDCAN bus in search of drives. 
# Any found drives will be printed out by the ping() method.
candle = pyCandle.Candle(pyCandle.CAN_BAUD_1M,True)
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
candle.controlMd80Mode(ids[0], pyCandle.IMPEDANCE)     
candle.controlMd80Mode(ids[1], pyCandle.IMPEDANCE)     
# Enable the drive
candle.controlMd80Enable(ids[0], True);  
candle.controlMd80Enable(ids[1], True);  

candle.begin()

start_time = time.time()
while (time.time() - start_time) < 5:
    q2_dot = candle.md80s[0].getVelocity() 
    if abs(q2_dot) > 10.: # Limit to 10 rad/s
        candle.md80s[0].setTargetTorque(0.) # u2
        candle.md80s[1].setTargetTorque(0.) # u1
    else:
        candle.md80s[0].setTargetTorque(0.2) # u2   
        candle.md80s[1].setTargetTorque(0.2) # u1

candle.end()

sys.exit("EXIT SUCCESS")
