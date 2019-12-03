from easygopigo3 import EasyGoPiGo3
from di_sensors.easy_inertial_measurement_unit import EasyIMUSensor
from di_sensors.easy_distance_sensor import EasyDistanceSensor
from time import sleep

class RudolphBot:
	def __init__(self):
		self.gpg = EasyGoPiGo3()
		self.sensor = EasyIMUSensor(port='AD2')
		self.target_heading = self.sensor.safe_north_point()
		self.distance_sensor = self.gpg.init_distance_sensor("GPG3_AD1")
		
		print("current heading: %f" % self.get_current_heading())

	def get_current_heading(self):
		heading, _, _ = self.sensor.safe_read_euler()
		return heading
		
	def visit_santa(self):
		obstacle_distance = self.distance_sensor.read_inches()
		print("Nearest Obstacle: %f" % obstacle_distance)
		
		if obstacle_distance < 6:
			print("I'll never see Santa with all these roadblocks!")
		else:
			print("I'm on my way Comet, don't eat my pancakes!")
		
if __name__ == "__main__":
	nb = RudolphBot()
	nb.visit_santa()
