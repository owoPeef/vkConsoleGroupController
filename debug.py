import os
import glob
from datetime import datetime

class Logger():
	def directoryCreate(self):
		try:
			os.makedirs(os.getcwd() + "\\Logs")
		except FileExistsError:
			pass
		finally:
			self.logCreate()
	def logCreate(self):
		os.open(os.getcwd() + "\\Logs\\" + str(datetime.now().strftime("%m.%d.%Y_%H.%M.%S")) + ".txt", os.O_RDWR | os.O_CREAT)
		self.lineLog("Bot started")
	def lineLog(self, message):
		list_of_files = glob.glob(os.getcwd() + '\\Logs\\*')
		latest_file = os.open(max(list_of_files, key=os.path.getctime), os.O_APPEND | os.O_RDWR)
		full_message = "[" + str(datetime.now().strftime('%d.%m.%Y %H:%M:%S')) + "] " + str(message)
		os.write(latest_file, str.encode(full_message + "\n"))