from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *



hub = PrimeHub()
AB = MotorPair('A','B')

E = Motor('E') 
F = Motor('F') 
leftSensor = ColorSensor('C')
rightSensor = ColorSensor('D')
rightMotor = Motor('B')
timer = Timer()

#turning
def getHeading():
    heading = hub.motion_sensor.get_yaw_angle()
    if(heading<0):
        heading+=360
    return(heading)

def turnToHeading(heading=0,speed=100):

    acceptableError = 3
    stopErrorSetting = 5
    
    allowedError = stopErrorSetting * (speed / 100)

    keepTurning = True#boolean
    while(keepTurning):
        # Should we turn left or right
        turnFactor = speed * leftOrRight(heading)
        print(turnFactor)
        AB.start_tank(turnFactor, turnFactor * -1)
        keepTurning = not (heading - allowedError <= getHeading() <= heading + allowedError)
    AB.stop()

    if (abs(getHeading() - heading) > acceptableError):
        print ("Outside allowed: %s, %s, %s" % (getHeading(), heading, acceptableError))
        turnToHeading(heading, speed/2)
    else:
        print("Inside allowed: %s, %s, %s" % (getHeading(), heading, acceptableError))

def leftOrRight(goal):
    current = getHeading()
    if current < goal:
        if goal - current < 180:
            return 1    # right
        else:
            return -1   # left
    else:
        if current - goal < 180:
            return -1   # left
        else:
            return 1    # right

'''def turn(degrees=0, speed=100):
    real_degrees = degrees*.95
    yaw = getHeading()
    AB.start_tank(speed,speed*-1)
    while(abs(yaw)<real_degrees):
        yaw = hub.motion_sensor.get_yaw_angle()
    AB.stop()

def left(degrees=0, speed=100):
    turn(degrees,speed*-1)

def right(degrees=0, speed=100):
    turn(degrees,speed)'''

#line following
def find_line():
    AB.start(0,30)
    while(leftSensor.get_reflected_light() > 50.0):
        pass
    AB.stop()

def single_follow(duration, correction_factor):
    find_line()
    timer.reset()
    while timer.now() < duration:
        error = leftSensor.get_reflected_light() - 50
        correction = error * correction_factor
        AB.start_tank_at_power(int(basePower + correction), int(basePower - correction))
    AB.stop()

def double_follow(duration):
    correction_factor = 0.3
    find_line()
    timer.reset()
    while timer.now() < duration:
        error = leftSensor.get_reflected_light() - rightSensor.get_reflected_light()
        correction = error * correction_factor
        AB.start_tank_at_power(int(basePower + correction), int(basePower - correction))
    AB.stop()

#driving
def driveSeconds(duration,heading):
    turn(heading)
    correction_factor = 3
    timer.reset()
    while timer.now() < duration:
        error = hub.motion_sensor.get_yaw_angle()
        correction = error * correction_factor
        AB.start_tank_at_power(int(basePower - correction), int(basePower + correction))
    AB.stop()

def driveDistance(distance,heading):
    cm_per_degree = (17.5 / 360) * 1.0 
    base_power = 30 
    turnToHeading(heading)
    rightMotor.set_degrees_counted(0)
    correction_factor = 3
    traveled = 0
	#lightMatrix.show_image("ARROW_N")
    while traveled < distance:
        error = hub.motion_sensor.get_yaw_angle()
        correction = error * correction_factor
        AB.start_tank_at_power(int(base_power - correction), int(base_power + correction))
        traveled = cm_per_degree * rightMotor.get_degrees_counted()
        print("Traveled: %s" % traveled)
    motorPair.stop()


def flyInit():
    F.set_degrees_counted(0)


def flySet(setting):
    current = F.get_degrees_counted()
    setting = setting*-1
    if (current > setting):
        F.run_to_degrees_counted(setting, -20)
    else:
        F.run_to_degrees_counted(setting, 20)

    
#def flymove(pos, speed):

flyInit()

def swordInit():
    E.set_degrees_counted(0)

def swordSet(setting):
    setting = setting * -1
    current = E.get_degrees_counted()
    if (current > setting):
        E.run_to_degrees_counted(setting, -10)
    else:
        E.run_to_degrees_counted(setting, 10)

swordInit()
swordSet(60)
wait_for_seconds(2)
swordSet(0)
exit(0)

'''flySet(180)

wait_for_seconds(1)

flySet(270)

wait_for_seconds(2)

flySet(90)

wait_for_seconds(2)

flySet(0)'''





#def stickInit():


#
#driveDistance(49,0)
#driveDistance(0,13)
#turnToHeading(335,100)

