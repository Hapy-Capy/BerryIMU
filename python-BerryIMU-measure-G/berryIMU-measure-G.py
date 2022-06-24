import time
import IMU
import sys, signal

def handle_ctrl_c(signal, frame):
    print(" ")
    print("cal_accXmin = %i"%  (accXmin))
    print("cal_accYmin = %i"%  (accYmin))
    print("cal_accZmin = %i"%  (accZmin))
    print("cal_accXmax = %i"%  (accXmax))
    print("cal_accYmax = %i"%  (accXmax))
    print("cal_accZmax = %i"%  (accZmax))
    sys.exit(130) # 130 is standard exit code for ctrl-c

accXmin = 32767
accYmin = 32767
accZmin = 32767
accXmax = -32767
accYmax = -32767
accZmax = -32767

cal_accXmin = 57
cal_accYmin = 0
cal_accZmin = 4061
cal_accXmax = 132
cal_accYmax = 132
cal_accZmax = 4358

IMU.detectIMU()     #Detect if BerryIMU is connected.
if(IMU.BerryIMUversion == 99):
    print(" No BerryIMU found... exiting ")
    sys.exit()
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

#This will capture exit when using Ctrl-C
signal.signal(signal.SIGINT, handle_ctrl_c)

while True:
    #Read the accelerometer,gyroscope and magnetometer values
    ACCx = IMU.readACCx()
    ACCy = IMU.readACCy()
    ACCz = IMU.readACCz()

    ACCx -= (cal_accXmin + cal_accXmax) / 2
    ACCy -= (cal_accYmin + cal_accYmax) / 2
    ACCz -= (cal_accZmin + cal_accZmax) / 2

    yG = (ACCx * 0.244)/1000 * 9.8066
    xG = (ACCy * 0.244)/1000 * 9.8066
    zG = (ACCz * 0.244)/1000 * 9.8066
    print("##### X = %fm/s^2  ##### Y =   %fm/s^2  ##### Z =  %fm/s^2  #####" % ( yG, xG, zG))

    if ACCx > accXmax:
        accXmax = ACCx
    if ACCy > accYmax:
        accYmax = ACCy
    if ACCz > accZmax:
        accZmax = ACCz
    if ACCx < accXmin:
        accXmin = ACCx
    if ACCy < accYmin:
        accYmin = ACCy
    if ACCz < accZmin:
        accZmin = ACCz
    print((" accXmin  %i  accYmin  %i  accZmin  %i  ## accXmax  %i  accYmax  %i  accZmax %i  "\
            %(accXmin,accYmin,accZmin,accXmax,accYmax,accZmax)))

    #slow program down a bit, makes the output more readable
    time.sleep(0.03)
