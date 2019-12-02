from easygopigo3 import EasyGoPiGo3
from time import sleep

class WanderBot:
	def __init__(self):
		self.gpg = EasyGoPiGo3()
		self.sensor = self.gpg.init_distance_sensor("GPG3_AD1")
		self.servo = servo = self.gpg.init_servo("SERVO1")
		
		self._look_around()
		self.angles = [10, 90, 170]
	
	def _look_around(self):
		print("looking around...")
		self.servo.rotate_servo(1)
		sleep(0.3)
		self.servo.rotate_servo(179)
		sleep(0.5)
		self.servo.reset_servo()
		
		wall_distance = self.sensor.read_inches()
		print("there is a wall %f inches away." % wall_distance)

	def find_nearest_wall(self):
		deltas = []
		for i in self.angles:
			servo_angle = i
			self.servo.rotate_servo(servo_angle)
			sleep(0.5)
			distance = self.sensor.read_inches()
			deltas.append(distance)
		
		closest = deltas.index(min(deltas))
		print('the closest wall is %f inches away at angle %f' % 
			  (deltas[closest], self.angles[closest]))
		self.servo.reset_servo()
		
		return self.angles[closest]
	
	def traverse(self):
		while self.sensor.read_inches() > 6:
			self.gpg.forward()
			
		self.gpg.stop()

	def goto_nearest_wall(self):
		drive_angle = self.find_nearest_wall()
		
		self.gpg.turn_degrees(90 - drive_angle)
		self.traverse()
	
	def find_next_wall(self):
		measurement = 1000
		last_measurement = 0
		turn_to = 0
		
		angle_set = [35, 30, 25, 20, 15, 10, 5, 1]
		distances = []
		for idx, angle in enumerate(angle_set):
			self.servo.rotate_servo(angle)
			sleep(0.3)
			measurement = self.sensor.read_inches()
			distances.append(measurement)
			
			if measurement > last_measurement:
				print("%f is greater than %f. Adjusting turn-to angle to %f" % 
				       (measurement, last_measurement, angle))
				turn_to = angle
				
			last_measurement = measurement
				
		self.gpg.turn_degrees(90 - turn_to)
		self.servo.reset_servo()
		self.traverse()
		
if __name__ == "__main__":
	wb = WanderBot()
	
	drive_angle = wb.goto_nearest_wall()
	
	for i in range(4):
		wb.find_next_wall()
	
	
