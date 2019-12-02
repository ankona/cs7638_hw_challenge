import time
import bisect
from easygopigo3 import EasyGoPiGo3

class EarBot:
	def __init__(self):
		self.gpg = EasyGoPiGo3()
		self.sensor = self.gpg.init_loudness_sensor("AD2")
		self.measurements = []
		self.loudness = 0
		self.thresholds = [600, 850, 950, 1500]
		self.colors = [(0, 255, 0), (255, 0, 255), (100, 65, 0), (255, 0, 0)]
		self.gpg.set_eye_color(self.colors[0])
		self.gpg.open_eyes()
		
	def blink(self):
		for i in range(3):
			self.gpg.close_eyes()
			time.sleep(0.5)
			self.gpg.open_eyes()
			time.sleep(0.5)
		#self.gpg.close_eyes()
		
	def sample(self, num_samples=10000):
		self.blink()
		self.loudness = 0
		self.measurements = []
		
		for i in range(num_samples):
			value = self.sensor.read()
			self.measurements.append(value)

		self.loudness = sum(self.measurements) / num_samples
		return self.measurements

	def notify(self):
		idx = bisect.bisect_left(self.thresholds, self.loudness)
		self.gpg.set_eye_color(self.colors[idx])
		self.blink()


if __name__ == "__main__":
	ep = EarBot()
	
	while True:
		measurements = ep.sample()
	
		print("Average Loudness: %i" % ep.loudness)
		print("Loudest Moment: %f" % max(measurements))
		print("Quietest Moment: %f\n" % min(measurements))
		ep.notify()
