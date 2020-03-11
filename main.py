# Itsy Bitsy M0 Express IO demo
# Welcome to CircuitPython 2.2 :) 
import board
""" pan & tilt thru servo kit """
import time
from adafruit_servokit import ServoKit
import gc
import time
#from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
#import pulseio
#from adafruit_motor import servo
#import adafruit_dotstar


# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)
# min_pulse=580, max_pulse=2480)
kit.servo[0].set_pulse_width_range(580, 2480) #X
kit.servo[1].set_pulse_width_range(580, 2480) #y


gc.collect()   # make some rooooom


# Analog input
analog3in = AnalogIn(board.A3) #x
analog4in = AnalogIn(board.A4) #y


# kit.servo[0].angle = 180
# time.sleep(1)
# kit.servo[1].angle = 0






# determine joystick movement
xzero = 34000
yzero = 33000
ydead = 2000
xdead = 2000
step = 1
min_x = 0
max_x = 180
min_y = 0
max_y = 180

def jdir(x,y,rcxprev,rcyprev):
    rcx=rcxprev
    rcy=rcyprev
#     LR takes priority over fwd/back
    if ( (x > (xzero + xdead)) | (x < (xzero-xdead))):
        if (x > xzero) & (rcxprev >= min_x + step):
            print("right", end="")
            rcx = rcxprev - 10
        elif (x < xzero) & (rcxprev <= max_x - step):
            print("left", end="")
            rcx = rcxprev + 10
            
    #print("zero: {} {}".format(yzero + ydead,yzero-ydead))
    if ( (y > (yzero + ydead)) | (y < (yzero-ydead))):
      if (y > yzero) & (rcyprev <= max_y - step):
        print("up", end="")
        rcy=rcyprev + 10
      elif (y < yzero) & (rcyprev >= min_y + step): 
        print("down", end="")
        rcy=rcyprev - 10
    print("\trcx:{} rcy:{} ".format(rcx,rcy),end="") 
    return rcx,rcy



# centre servos
rcxprev=90
rcyprev=90
kit.servo[0].angle = rcxprev #X
kit.servo[1].angle = rcyprev #Y
i=0
while True:
#   Read analog voltage on A1
#   print("A1: %0.2f" % getVoltage(analog1in), end="\t")

  x = analog4in.value
  y = analog3in.value
  print("X: {:5}".format(x), end="\t")
  print("Y: {:5}".format(y), end="\t")
  rcx,rcy=jdir(x,y,rcxprev,rcyprev)
  rcxprev = rcx
  rcyprev = rcy

  # sweep servos
  i = (i+1) % 5
  #print(i)
  #if (i==4):
  kit.servo[1].angle = rcy #Y
  kit.servo[0].angle = rcx #X
    
  time.sleep(0.005) #make bigger to slow down
  

  print("")
