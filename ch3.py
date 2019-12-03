from easygopigo3 import EasyGoPiGo3
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
	INITIAL_SPEED = 1.0 * 66.5 * (360 / 66.5)
	
	def __init__(self):
		self.gpg = EasyGoPiGo3()
		self.target_speed = 1.5 * 66.5 * (360 / 66.5)
		self.distance_sensor = self.gpg.init_distance_sensor("I2C")
		self.offset = self.distance_sensor.read_mm()
		self.gpg.set_speed(SpeedBot.INITIAL_SPEED)
		
		print('SpeedBot initialized. Offset is %f' % self.offset)

	def go_p(self):
		mm_per_wheel = 66.5
		deg_per_mm = 360 / 66.5
		last_distance = self.distance_sensor.read_mm()
		mm_from_wall = self.distance_sensor.read_mm()
		travelled = 0
		self.gpg.forward()
		
		while mm_from_wall < 800:
			sleep(0.5)
			mm_from_wall = self.distance_sensor.read_mm()
			#print('mm_from_wall: %f' % mm_from_wall)
			segment_mm = mm_from_wall - last_distance
			#print('segment_mm: %f' % segment_mm)
			#segment_mm = mm_from_wall - last_distance
			#print('2 * segment_mm * deg_per_mm: %f' % (2.0 * segment_mm * deg_per_mm))
			if segment_mm < 0:
				segment_mm = 0
			
			velocity = 2 * segment_mm * deg_per_mm
			last_distance = mm_from_wall
			
			cte = velocity - self.target_speed
			alpha = -cte * 0.3
			
			self.gpg.set_speed(self.gpg.get_speed() + alpha)
			
			print('v: %f, seg: %f, ld: %f, cte: %f, o: %f, ts: %f' % 
				  (velocity, segment_mm, last_distance, cte, self.offset, self.target_speed))
			
			
		self.gpg.stop()
		self.gpg.set_speed(180)
		wall = self.distance_sensor.read_mm() 
		while wall > self.offset + 50:
			#print('wall, offset: ', wall, self.offset)
			self.gpg.backward()
			wall = self.distance_sensor.read_mm() 
		self.gpg.stop()
	

	def go_pd(self):
		mm_per_wheel = 66.5
		deg_per_mm = 360 / 66.5
		last_distance = self.distance_sensor.read_mm()
		mm_from_wall = last_distance
		travelled = 0
		self.gpg.forward()
		cte_last = 0
		
		while mm_from_wall < 800:
			sleep(0.5)
			mm_from_wall = self.distance_sensor.read_mm()
			#print('mm_from_wall: %f' % mm_from_wall)
			segment_mm = mm_from_wall - last_distance
			#print('segment_mm: %f' % segment_mm)
			#segment_mm = mm_from_wall - last_distance
			#print('2 * segment_mm * deg_per_mm: %f' % (2.0 * segment_mm * deg_per_mm))
			if segment_mm < 0:
				segment_mm = 0
			
			velocity = 2 * segment_mm * deg_per_mm
			last_distance = mm_from_wall
			
			cte = velocity - self.target_speed
			differential = cte - cte_last
			alpha = -cte * 0.2 - (0.05 * differential)
			cte_last = cte
			
			if cte > 1000:
				continue
			
			print('v: %f, seg: %f, ld: %f, cte: %f, o: %f, ts: %f, ss: %f' % 
				  (velocity, segment_mm, last_distance, cte, self.offset, self.target_speed, self.gpg.get_speed()))
			
			self.gpg.set_speed(self.gpg.get_speed() + alpha)
			
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
	nb.go_pd()
	
	
		
