import requests, json, csv, time

class statAPI():
	apiKey = '*apiKey*'
	APIdisconnect = False
	totalErrors = 0
	def getAPIData(self):
		url = ''		
		apiEndpoint = 'https://example.getstat.com/api/v2/' + self.apiKey + '/keywords/list?site_id=####'
			
		headers = {
			'content-type':"application/json"
		}
		config = {
			'key':self.apiKey,
			'type':'backlinks_overview',
			'database':'us',
			'target_type':'domain',
			'target':url
		}
		try:
			print("Checking",url)
			HTTPrequest = requests.get(apiEndpoint)
			print(HTTPrequest.text)
		except requests.exceptions.SSLError:
			self.totalErrors = self.totalErrors + 1
			print('SSL error.  Total errors',self.totalErrors)
			if(self.totalErrors > 50):
				self.APIdisconnect = True
		except requests.exceptions.ConnectionError:
			print('API endpoint disconnected.  Total errors',self.totalErrors)
			self.APIdisconnect = True
	
					
Stat = statAPI()
Stat.getAPIData()
