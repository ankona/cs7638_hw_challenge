from easygopigo3 import EasyGoPiGo3
#from di_sensors.easy_inertial_measurement_unit import EasyIMUSensor
#from di_sensors import inertial_measurement_unit as imulib
from di_sensors.easy_distance_sensor import EasyDistanceSensor
from time import sleep, time

class MockGPG:
	def __init__(self):
		self.speed = 0
		
	def get_speed(self):
		return self.speed
		
	def set_speed(self, s):
		self.speed = s


class SpeedBot:
	#TAU = 0.2
	#OBS_SAFE_DIST = 12
	INITIAL_SPEED = 300
	
	def __init__(self):
		self.gpg = EasyGoPiGo3()
		#self.imu = imulib.InertialMeasurementUnit()
		self.target_speed = 100 # self.sensor.safe_north_point()
		self.distance_sensor = self.gpg.init_distance_sensor("GPG3_AD1")
		self.offset = self.distance_sensor.read_mm()
		self.gpg.set_speed(SpeedBot.INITIAL_SPEED)
		
		print('SpeedBot initialized. Offset is %f' % self.offset)

	def go(self):
		mm_per_wheel = 66.5
		deg_per_mm = 360 / mm_per_wheel
		last_distance = 0
		self.gpg.forward()
		
		#t_start = time()
		travelled = 0
		
		while travelled < 1200:
			#t_end = t_start - time()
			mm_from_wall = self.distance_sensor.read_mm()
			travelled = mm_from_wall - self.offset - last_distance
			if travelled < 0:
				travelled = 0

			velocity = travelled / deg_per_mm
			cte = velocity - self.target_speed
			alpha = -cte * 0.4
			
			print('alpha: %f, gpg.speed: %f, travelled: %f, cte: %f, velocity: %f, ld: %f, mm_from_wall: %f' % 
				  (alpha, self.gpg.speed, travelled, cte, velocity, last_distance, mm_from_wall))
			
			next_speed = self.gpg.speed + alpha
			#print('setting speed to:', next_speed)
			self.gpg.set_speed(next_speed)
			
			
			#print(self.gpg.get_speed(), cte, int(next_speed), int(travelled), int(velocity))
			last_distance = travelled
			sleep(1.0)
			
			
		self.gpg.stop()
		self.gpg.set_speed(180)
		wall = self.distance_sensor.read_mm() 
		while wall > self.offset + 50:
			#print('wall, offset: ', wall, self.offset)
			self.gpg.backward()
			wall = self.distance_sensor.read_mm() 
		self.gpg.stop()
		
if __name__ == "__main__":
	nb = SpeedBot()
	nb.go()
	
	
		
