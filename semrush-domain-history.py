import requests, json, csv, time

class semRush():
	apiKey = '***********************'
	reportURLs = []
	reportHeaders = []
	csvPath = ""
	csvData = {}
	APIdisconnect = False
	totalErrors = 0
	def processData(self):
		for index,thisURL in self.csvData.items():
			if(not self.APIdisconnect):
				if(thisURL[1] == ''):
					self.getAPIData(index)
					#time.sleep(0.5)
	def getAPIData(self,urlID):
		url = self.csvData[urlID][0]
				
		apiEndpoint = 'https://api.semrush.com/'

		headers = {
			'content-type':"application/json"
		}
		config = {
			'key':self.apiKey,
			'type':'domain_rank_history',
			'database':'us',
			'domain':url
		}
		try:
			print("Checking",url)
			HTTPrequest = requests.get(apiEndpoint, headers = headers, params = config)
			rows = HTTPrequest.text.split("\r\n")
			results = [thisRow.split(";") for thisRow in rows]
			self.reportHeaders = results.pop(0)
			if(results != []):
				urlData = [url]
				urlData.extend(results[0])
				self.csvData[urlID] = urlData
				self.writeCSVData()
		except requests.exceptions.SSLError:
			self.totalErrors = self.totalErrors + 1
			print('SSL error.  Total errors',self.totalErrors)
			if(self.totalErrors > 50):
				self.APIdisconnect = True
		except requests.exceptions.ConnectionError:
			print('API endpoint disconnected.  Total errors',self.totalErrors)
			self.APIdisconnect = True
	def getCSVData(self):
		with open(self.csvPath, 'r', encoding = "utf-8") as csv_file:
			csv_reader = csv.reader(csv_file, delimiter = ',')
			rowID = -1
			for row in csv_reader:
				if(rowID != -1):
					self.csvData[rowID] = row
				rowID = rowID + 1
	def writeCSVData(self):
		with open(self.csvPath, 'w', newline = '', encoding="utf-8") as csvfile:
			output = csv.writer(csvfile, delimiter=',', quotechar='"')
			header = ['URL']
			for thisHeader in self.reportHeaders:
				header.append(thisHeader)
			output.writerow(header)	
			
			for index,thisData in self.csvData.items():
				output.writerow(self.csvData[index])		
					
SEM = semRush()
SEM.csvPath = 'domain-cost.csv'
SEM.getCSVData()
SEM.processData()
