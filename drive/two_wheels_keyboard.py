import signal,sys,tty,termios
import RPi.GPIO as GPIO
import time
from time import sleep
from enum import Enum
from evdev import InputDevice, categorize, ecodes

E_ON = 100
E_OFF = 0

TRIG = 13
ECHO = 11

dev = InputDevice('/dev/input/event1')
GPIO.setmode(GPIO.BOARD)

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

def compute_proximity():
	GPIO.output(TRIG, False)
	print "Waiting For Sensor To Settle"
#	time.sleep(1)


	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)

	while GPIO.input(ECHO)==0:
	  pulse_start = time.time()

	while GPIO.input(ECHO)==1:
	  pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start

	distance = pulse_duration * 17150

	distance = round(distance, 2)

	print "Distance:",distance,"cm"

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
			pwm_instance.ChangeDutyCycle(duty_cycle)
		else:
			pwm_instance.start(duty_cycle)
		self.started[pwm_instance] = True

	def move_back(self, absolute_speed = 100):
		self._setDutyCycle(self.A, 0)
		self._setDutyCycle(self.B, absolute_speed)
		self._setDutyCycle(self.E, E_ON)

	def move_forward(self, absolute_speed = 100):
		self._setDutyCycle(self.A, absolute_speed)
		self._setDutyCycle(self.B, 0)
		self._setDutyCycle(self.E, E_ON)

	def stop(self):
		self.A.stop()
		self.B.stop()
		self.E.stop()
		self.started = {self.A: False, self.B: False, self.E: False}		

BUS_DEFAULT_SPEED = 100

class Bus(object):
	condition = "new"
	def __init__(self):
		self.l = Wheel(35, 37, 33)
		self.r = Wheel(38, 40, 36)
	
	def hit_the_gas(self):
		#compute_proximity()
		print "Done computing proximity"
		self.l.move_forward(BUS_DEFAULT_SPEED)
		self.r.move_forward(BUS_DEFAULT_SPEED)

	def steer_left(self):
		self.l.move_back(BUS_DEFAULT_SPEED)
		self.r.move_forward(BUS_DEFAULT_SPEED)

	def steer_right(self):
		self.l.move_forward(BUS_DEFAULT_SPEED)
		self.r.move_back(BUS_DEFAULT_SPEED)

	def rear_it(self):
		self.l.move_back()
		self.r.move_back()
	
	def stop(self):
		self.l.stop();
		self.r.stop();

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

def signal_handler(signal, frame):
   	print 'You pressed Ctrl+C!'
	GPIO.cleanup()
	sys.exit(0)


def console():
	#signal.signal(signal.SIGINT, signal_handler)
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

