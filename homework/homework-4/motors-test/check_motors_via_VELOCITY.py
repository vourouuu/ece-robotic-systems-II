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

'''
#1 Movement Limits
- profileVelocity: The maximum speed the motor is allowed to reach during a move.
- profileAcceleration: How fast the motor speeds up to reach the profileVelocity.
- profileDeceleration: How fast the motor slows down as it approaches the target position.

#2 Safety and Precision
- quickStopDeceleration: The deceleration rate used during an emergency stop
                         (usually much higher than profileDeceleration).
- positionWindow: The "tolerance" for position. The motor considers the target reached
                  if it is within this distance from the goal.
- velocityWindow: The "tolerance" for speed. The motor considers the target velocity reached
                  if the actual speed is within this range.
'''
candle.writeMd80Register(ids[0], pyCandle.Md80Reg_E.positionWindow, 0.05)
candle.writeMd80Register(ids[0], pyCandle.Md80Reg_E.velocityWindow, 1.0)
candle.writeMd80Register(ids[0], pyCandle.Md80Reg_E.profileAcceleration, 10.0)
candle.writeMd80Register(ids[0], pyCandle.Md80Reg_E.profileDeceleration, 5.0)
candle.writeMd80Register(ids[0], pyCandle.Md80Reg_E.profileVelocity, 15.0)
candle.writeMd80Register(ids[0], pyCandle.Md80Reg_E.quickStopDeceleration, 200.0)

candle.writeMd80Register(ids[1], pyCandle.Md80Reg_E.positionWindow, 0.05)
candle.writeMd80Register(ids[1], pyCandle.Md80Reg_E.velocityWindow, 1.0)
candle.writeMd80Register(ids[1], pyCandle.Md80Reg_E.profileAcceleration, 10.0)
candle.writeMd80Register(ids[1], pyCandle.Md80Reg_E.profileDeceleration, 5.0)
candle.writeMd80Register(ids[1], pyCandle.Md80Reg_E.profileVelocity, 15.0)
candle.writeMd80Register(ids[1], pyCandle.Md80Reg_E.quickStopDeceleration, 200.0)

# Reset encoder at current position
candle.controlMd80SetEncoderZero(ids[0])      
candle.controlMd80SetEncoderZero(ids[1])      
# Set mode to impedance control
candle.controlMd80Mode(ids[0], pyCandle.VELOCITY_PROFILE)     
candle.controlMd80Mode(ids[1], pyCandle.VELOCITY_PROFILE)     
# Enable the drive
candle.controlMd80Enable(ids[0], True);  
candle.controlMd80Enable(ids[1], True);  

candle.begin()

candle.md80s[0].setProfileAcceleration(1.0)
candle.md80s[0].setProfileVelocity(20.0)
candle.md80s[0].setTargetVelocity(10.0)

while not candle.md80s[0].isTargetVelocityReached():
    time.sleep(1)

candle.md80s[0].setProfileAcceleration(20.0)
candle.md80s[0].setProfileVelocity(50.0)
candle.md80s[0].setTargetVelocity(20.0)

while not candle.md80s[0].isTargetVelocityReached():
    time.sleep(1)

candle.end()
sys.exit("EXIT SUCCESS")
