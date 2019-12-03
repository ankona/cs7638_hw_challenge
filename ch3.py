from easygopigo3 import EasyGoPiGo3
from di_sensors.easy_inertial_measurement_unit import EasyIMUSensor
from di_sensors.easy_distance_sensor import EasyDistanceSensor
from time import sleep

class RudolphBot:
	TAU = 0.4
	OBS_SAFE_DIST = 12
	
	def __init__(self):
		self.gpg = EasyGoPiGo3()
		self.sensor = EasyIMUSensor(port='AD2')
		self.target_heading = 0 # self.sensor.safe_north_point()
		self.distance_sensor = self.gpg.init_distance_sensor("GPG3_AD1")
		
		print("current heading: %f" % self.get_current_heading())
		print("target heading: %f" % self.target_heading) 

	def get_current_heading(self):
		heading, _, _ = self.sensor.safe_read_euler() 
		heading, a, b = self.sensor.safe_read_euler() 
		print(heading, a, b)
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
				
			#self.gpg.forward() # (5)
			#sleep(0.3)
			#sleep(1.0)
			
			alpha = self.p_controller_get_angle()
			#if alpha > 15 or alpha < -15:
			#	alpha = 15
			if abs(alpha) < 1:
				break
				
			#self.gpg.turn_degrees(alpha)
			if alpha > 0:#
				print('drive right')
				self.gpg.right()
				#self.gpg.steer(50, 100)
				#self.gpg.orbit(-alpha, 30)
			else:
				print('drive left')
				self.gpg.left()
				#self.gpg.steer(100, 50)
				#self.gpg.orbit(alpha, 30)
			
			sleep(0.2)
			print('going straight for a bit...')	
			self.gpg.drive_cm(100.0 * (abs(alpha) / 100))
			
			
		self.stop()
		
	def p_controller_get_angle(self):
		current = self.get_current_heading()
		#print('current heading is: %f' % current)
		
		if current >= 180:
			cte = 360 - current
		else:
			cte = -current
		
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
	
	
		
