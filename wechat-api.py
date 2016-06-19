# Author: Xinxing Jiang@Palm Science Inc.

import json
import requests

class WeChatAPI(object):
	configFile = "wechat-config.json"
	commentSyntax = "//"
	horizontalRule = "----------------"

	requestAccessTokenUrl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}"
	requestUserListUrl = "https://api.weixin.qq.com/cgi-bin/user/get?access_token={0}"
	successStatusCode = 200

	# get APPID and AppSecret
	def loadConfig(self):
		self.log(self.horizontalRule)
		self.log("Loading config")		
		inputFileHandler = open(self.configFile)
		# skip comment
		while True:
			line = inputFileHandler.readline()			
			if not line.startswith(self.commentSyntax):
				config = line
				break		
		content = json.loads(config)
		self.appID = content["APPID"]
		self.appSecret = content["AppSecret"]
		inputFileHandler.close()
		self.log("Done")

	# get access token
	def requestAccessToken(self):
		self.log(self.horizontalRule)
		self.log("Request access token")
		response = requests.get(self.requestAccessTokenUrl.format(self.appID, self.appSecret))
		if self.checkStatusCode(response):
			content = json.loads(response.content)
			self.accessToken = self.getOrElse(content, "access_token")
		self.log("Done")

	# get user list
	def requestTotalUser(self):
		self.log(self.horizontalRule)
		self.log("Get total user")
		response = requests.get(self.requestUserListUrl.format(self.accessToken))
		if self.checkStatusCode(response):
			content = json.loads(response.content)
			self.totalUser = self.getOrElse(content, "total")
		self.log("Done")
		self.log(self.horizontalRule)
		self.log("Total user: {0}".format(self.totalUser if self.__dict__.has_key("totalUser") else "who knows"))

	# get key, or log error message 
	def getOrElse(self, content, key):
		try:
			return content[key]
		except Exception:
			self.log("undefined key: {0}".format(key))		

	# check whether response status is 200 OK
	def checkStatusCode(self, response):
		self.log("response status code: {0}".format(response.status_code))
		return response.status_code == self.successStatusCode	

	# log message
	def log(self, s):
		print s

if __name__ == "__main__":
	weChatAPI = WeChatAPI()
	weChatAPI.loadConfig()
	weChatAPI.requestAccessToken()
	weChatAPI.requestTotalUser()