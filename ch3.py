from easygopigo3 import EasyGoPiGo3
from di_sensors.easy_inertial_measurement_unit import EasyIMUSensor
from di_sensors.easy_distance_sensor import EasyDistanceSensor
from time import sleep

class RudolphBot:
	TAU = 0.4
	OBS_SAFE_DIST = 6
	
	def __init__(self):
		self.gpg = EasyGoPiGo3()
		self.sensor = EasyIMUSensor(port='AD2')
		self.target_heading = self.sensor.safe_north_point()
		self.distance_sensor = self.gpg.init_distance_sensor("GPG3_AD1")
		
		print("current heading: %f" % self.get_current_heading())
		print("target heading: %f" % self.target_heading) 

	def get_current_heading(self):
		heading, _, _ = self.sensor.safe_read_euler() 
		return heading
	
	def check_for_obstacles(self):
		obstacle_distance = self.distance_sensor.read_inches()
		
		if obstacle_distance < RudolphBot.OBS_SAFE_DIST:
			print("I'll never see Santa with all these roadblocks!")
			self.gpg.stop()
			return True

		print("I'm on my way Comet, don't eat my pancakes!")
		return False

	def visit_santa(self):
		while True:
			if self.check_for_obstacles():
				break
				
			self.gpg.forward() # (5)
			#sleep(0.5)
			#sleep(1.0)
			
			alpha = self.p_controller_get_angle()
			#if alpha > 15 or alpha < -15:
			#	alpha = 15
			if abs(alpha) < 1:
				break
				
			#self.gpg.turn_degrees(alpha)
			if abs(alpha) > 0:
				left()
			else:
				right()
			
		self.stop()
		
	def p_controller_get_angle(self):
		current = self.get_current_heading()
		#print('current heading is: %f' % current)
		
		if current >= 180:
			cte = 360 - current
		else:
			cte = -current
		
		#cte = self.sensor.safe_north_point()
		
		print('current cte is: %f' % cte)
		
		alpha = RudolphBot.TAU * cte
		print('p-controller alpha value is: %f' % alpha)
		
		return alpha
		
	def stop(self):
		self.gpg.stop()
		
if __name__ == "__main__":
	nb = RudolphBot()
	nb.visit_santa()
	nb.stop()
	
	
		
