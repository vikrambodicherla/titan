import sys,tty,termios
import RPi.GPIO as GPIO
from time import sleep
from enum import Enum

E_ON = 100
E_OFF = 0

GPIO.setmode(GPIO.BOARD)

class Wheel(object):
	condition = "new"
	def __init__(self, A, B, E):
		GPIO.setup(A, GPIO.OUT)
		GPIO.setup(B, GPIO.OUT)
		GPIO.setup(E, GPIO.OUT)

		self.Eport = E
		self.A = GPIO.PWM(A, 100)
		self.B = GPIO.PWM(B, 100)
		self.E = GPIO.PWM(E, 100)

		self.started = {self.A: False, self.B: False, self.E: False}

	def _setDutyCycle(self, pwm_instance, duty_cycle):
		if self.started[pwm_instance]:
			print "Wheel ", pwm_instance, self.Eport, " changing to ", duty_cycle
			pwm_instance.ChangeDutyCycle(duty_cycle)
		else:
			print "Wheel ", pwm_instance, self.Eport, " starting at ", duty_cycle
			pwm_instance.start(duty_cycle)
		self.started[pwm_instance] = True

	def move_back(self, absolute_speed = 100):
		print "Wheel back: ", self.Eport, absolute_speed
		self._setDutyCycle(self.A, absolute_speed)
		self._setDutyCycle(self.B, 0)
		self._setDutyCycle(self.E, E_ON)

	def move_forward(self, absolute_speed = 100):
		print "Wheel fwd: ", self.Eport, absolute_speed
		self._setDutyCycle(self.A, 0)
		self._setDutyCycle(self.B, absolute_speed)
		self._setDutyCycle(self.E, E_ON)

	def stop(self):
		self.E.stop()

class MotionState(Enum):
	moving_forward = 1
	moving_backward = -1
	stationary = 0

BUS_DEFAULT_SPEED = 100
BUS_TURNWHEEL_SPEED = 15

class Bus(object):
	condition = "new"
	def __init__(self):
		self.fl = Wheel(35, 37, 33)
		self.rl = Wheel(38, 40, 36)
		self.fr = Wheel(13, 15, 11)
		self.rr = Wheel(22, 18, 16)
		self.motion_state = MotionState.stationary
	
	def hit_the_gas(self):
		self.fl.move_forward(BUS_DEFAULT_SPEED)
		self.rl.move_forward(BUS_DEFAULT_SPEED)
		self.fr.move_forward(BUS_DEFAULT_SPEED)
		self.rr.move_forward(BUS_DEFAULT_SPEED)
		self.motion_state = MotionState.moving_forward

	def steer_left(self):
		if self.motion_state is MotionState.moving_forward:
			#self.fl.move_forward(BUS_TURNWHEEL_SPEED)
			#self.rl.move_forward(BUS_TURNWHEEL_SPEED)
			self.fl.move_back(BUS_TURNWHEEL_SPEED)
			self.rl.move_back(BUS_TURNWHEEL_SPEED)
		elif self.motion_state is MotionState.moving_backward:
			self.fl.move_back(BUS_TURNWHEEL_SPEED)
			self.rl.move_back(BUS_TURNWHEEL_SPEED)		

	def steer_right(self):
		if self.motion_state is MotionState.moving_forward:
			self.fr.move_forward(BUS_TURNWHEEL_SPEED)
			self.rr.move_forward(BUS_TURNWHEEL_SPEED)
		elif self.motion_state is MotionState.moving_backward:
			self.fr.move_back(BUS_TURNWHEEL_SPEED)
			self.rr.move_back(BUS_TURNWHEEL_SPEED)

	def rear_it(self):
		self.fl.move_back()
		self.rl.move_back()
		self.fr.move_back()
		self.rr.move_back()
		self.motion_state = MotionState.moving_backward
	
	def stop(self):
		self.fl.stop();
		self.rl.stop();
		self.fr.stop();
		self.rr.stop();
		self.motion_state = MotionState.stationary

	def turn_off(self):
		GPIO.cleanup()

class _Getch:
	def __call__(self):
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
                	tty.setraw(sys.stdin.fileno())
                	ch = sys.stdin.read(3)
            	finally:
                	termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch        

def console():
	bus = Bus()

	while True:
        	inkey = _Getch()
        	while(1):
                	k=inkey()
                	if k!='1':break
        	if k=='\x1b[A':
                	print "up"
                	bus.hit_the_gas()
        	elif k=='\x1b[B':
                	print "down"
                	bus.rear_it()
        	elif k=='\x1b[C':
                	print "right"
                	bus.steer_right()
        	elif k=='\x1b[D':
                	print "left"
                	bus.steer_left()
        	else:
                	print "not an arrow key!"
                	bus.stop()
			#bus.turn_off();
			break;

if __name__ == "__main__":
    console()

