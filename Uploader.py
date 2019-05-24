import subprocess
import os
import time
import json
import platform
import datetime
from pprint import pprint
from progressbar import ProgressBar
try:
  import ctypes.wintypes
except:
  pass

class Uploader:

	def __init__(self, args):
		self.userDefinedPath = args[0]
		self.visibility = args[1]
		self.demoPath = self.getUserDemoPath(self.userDefinedPath)
		self.responseList = {}
		self.pbar = ProgressBar()
		self.getUploadParameters()
		self.fileList = self.getFileList()
		self.replayList = self.filterFileList(self.fileList)

	def getUploadParameters(self):
		self.uploadURL = 'https://ballchasing.com/api/v2/upload?visibility=' + self.visibility
		self.authFilepath = 'Resources/auth'
		self.authID = self.getAuthID()
		self.tempResponsePath = 'Resources/Logs/tempResponse'
		self.responseLogPath = 'Resources/Logs/Responses'

	def getAuthID(self):
		with open(self.authFilepath, 'r') as file:
			authID = file.read()
		return authID

	# Finds the path Rocket League uses to store the replay files on the system
	# Default windows path: C:/Users/%USERNAME%/Documents/My Games/Rocket League/TAGame/Demos/
	# Default macos path: '~/Library/Application Support/Rocket League/TAGame/Demos'
	def getUserDemoPath(self, userDefinedPath=None):
		if userDefinedPath is not None:
			return userDefinedPath

		if platform.system() == 'Windows':
			CSIDL_PERSONAL= 5
			SHGFP_TYPE_CURRENT= 0
			buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
			ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_PERSONAL, 0, SHGFP_TYPE_CURRENT, buf)
			dPath = str(buf.value) + '\\My Games\\Rocket League\\TAGame\\Demos\\'
			return dPath
		elif platform.system() == 'Darwin':
			dPath = '/Library/Application Support/Rocket League/TAGame/Demos/'
			return dPath

	def getFileList(self, demoPath=None):
		if demoPath is None:
			demoPath = self.demoPath
		return [(x[0], time.ctime(x[1].st_ctime), os.path.getsize(x[0])) for x in sorted([((demoPath + fn), os.stat((demoPath + fn))) for fn in os.listdir(demoPath)], key = lambda x: x[1].st_ctime)]

	def filterFileList(self, fileList):
		filteredList = []
		for replay in fileList:
			if replay[2] > 5000 and ('.replay' in replay[0]):
				filteredList.append(replay)
		return filteredList

	def getTempResponse(self):
		if os.path.exists(self.tempResponsePath):
			return self.readJSON()
		return None

	def readJSON(self):
		with open(self.tempResponsePath, 'r') as file:
			response = json.load(file)
		return response

	def writeJSON(self, data):
		logPath = self.responseLogPath + str(datetime.datetime.now().strftime(" %Y-%m-%d %H-%M-%S"))
		with open(logPath, 'w') as file:
			json.dump(data, file, indent=4)

	def logResponses(self):
		self.writeJSON(self.responseList)

	def upload(self):
		self.responseList['UploadInformation'] = {'Path':self.demoPath, 'Visibility':self.visibility, 'ReplayCount':len(self.replayList)}
		for replay in self.pbar(self.replayList):
			subprocess.call(['curl', '-s', '-o', self.tempResponsePath, '-F', 'file=@' + replay[0],'-H', 'Authorization:' + self.authID, self.uploadURL], shell=False)
			tempResponse = self.getTempResponse()
			self.responseList[replay[0]] = tempResponse
		self.logResponses()