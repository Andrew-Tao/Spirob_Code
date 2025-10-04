import gpiozero
from hx711 import HX711
import time
import threading
import os
import json
import matplotlib.pyplot as plt
import threading
import time
import numpy as np
class Load_Cell:
	def __init__(self	
	):
		self.hx = HX711(14,15)
		self.path = None
		self.load_collection = []
		self.hx.set_reading_format("MSB", "MSB")
		self.hx.set_reference_unit(100)
		self.hx.reset()
		self.hx.tare()
		self.sampling_freq = 20
	
	def start(self):
		def get_load():
			try:
				while True:
					start_time = time.time()
					val = self.hx.read_long()  # average over 5 samples
					now = time.time()
					
					sleep_for = (1/self.sampling_freq)- ((now - start_time)% (1/self.sampling_freq))
					if sleep_for > 0:
						time.sleep(sleep_for)
					self.load_collection.append(val)
			except KeyboardInterrupt:
				print("KeyboardInterrupt")
			finally:
				pass
		t_load = threading.Thread(target = get_load,daemon = True)
		#t_load.start()
	def end(self):
		with open(self.path,"w") as f:
			json.dump(self.load_collection,f)
		
		x_data = np.array([])
		for i in range(len(self.load_collection)):
			x_data = np.append(x_data,i)
			print(i)
		data = np.array(self.load_collection)
		print(len(data))
		"""
		plt.plot(x_data/10,data/100000)
		plt.xlabel("Time(s)")
		plt.ylabel("Stress (Pa)")
		#plt.ylim(0,20)
		plt.grid(True)
		plt.tight_layout()
		plt.legend()
	
		plt.show()
		"""
		
