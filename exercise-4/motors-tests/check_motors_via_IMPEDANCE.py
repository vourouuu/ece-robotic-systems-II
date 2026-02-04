import pyCandle
import sys
import time

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
candle.controlMd80Mode(ids[0], pyCandle.IMPEDANCE)     
candle.controlMd80Mode(ids[1], pyCandle.IMPEDANCE)     
# Enable the drive
candle.controlMd80Enable(ids[0], True);  
candle.controlMd80Enable(ids[1], True);  

# Begin update loop (it starts in the background)
candle.begin()

print("------------- GET CURRENT VALUES -------------")
i = 0
for id in ids:
    q = candle.md80s[i].getPosition()
    print(f"- (id={id}) - Position: {q:.3f} rad")
    
    u = candle.md80s[i].getVelocity()
    print(f"- (id={id}) - Velocity: {u:.3f} rad/sec")

    tau = candle.md80s[i].getTorque()
    print(f"- (id={id}) - Torque: {tau:.3f} Nm")
    
    i = i + 1
print("---------------------------------------------\n")

print("----------------- SET VALUES ----------------")
# Targer q of upper motor
candle.md80s[0].setTargetPosition(-1.57) # -1.57 rad = -90 degrees (q2)
candle.md80s[1].setTargetPosition(1.57)  #  1.57 rad =  90 degrees (q1)

start_time = time.time()
while (time.time() - start_time) < 2:
    q2 = candle.md80s[0].getPosition()
    u2 = candle.md80s[0].getVelocity()
    tau2 = candle.md80s[0].getTorque()

    print(f"- (id={375}) - Position: {q2:.3f} rad")
    print(f"- (id={375}) - Velocity: {u2:.3f} rad")
    print(f"- (id={375}) - Torque: {tau2:.3f} rad")
    
    q1 = candle.md80s[1].getPosition()
    u1 = candle.md80s[1].getVelocity()
    tau1 = candle.md80s[1].getTorque()

    print(f"- (id={399}) - Position: {q1:.3f} rad")
    print(f"- (id={399}) - Velocity: {u1:.3f} rad")
    print(f"- (id={399}) - Torque: {tau1:.3f} rad\n")

    time.sleep(0.1)
print("---------------------------------------------")

# Close the update loop
candle.end()

sys.exit("EXIT SUCCESS")
