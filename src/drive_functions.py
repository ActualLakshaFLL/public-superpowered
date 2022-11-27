from spike import PrimeHub, MotorPair, Motor, ColorSensor, LightMatrix

motorPair = MotorPair("A", "B")

leftMotor = Motor("A")

primeHub = PrimeHub()

lightMatrix = primeHub.light_matrix

leftSensor = ColorSensor("C")
rightSensor = ColorSensor("D")

base_power = 40.0

def single_follow(distance):
    leftMotor.set_degrees_counted(0)

    goal_degrees = (distance / 17.5) * 360

    correction_factor = 0.3
    while leftMotor.get_degrees_counted() < goal_degrees:
        error = leftSensor.get_reflected_light() - 50
        correction = error * correction_factor
        motorPair.start_tank_at_power(int(base_power + correction), int(base_power - correction))
    motorPair.stop()

def find_line():
    motorPair.start(0, 40)
    while leftSensor.get_reflected_light() > 40:
        pass
    motorPair.stop()

		
def double_follow(duration):
    timer.reset()
    correction_factor = 0.2

    while timer.now() < duration:
        error = leftSensor.get_reflected_light() - rightSensor.get_reflected_light()
        correction = error * correction_factor
        motorPair.start_tank_at_power(int(basePower + correction), int(basePower - correction))
    motorPair.stop()
		
		
		
		
