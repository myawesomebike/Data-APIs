import http.client, urllib.request, urllib.parse, urllib.error, base64, json, requests, csv, time

class azureVisionAPI():
	apiRegion = 'eastus'
	apiURL = 'https://{}.api.cognitive.microsoft.com/vision/v1.0/analyze'.format(apiRegion)
	apiKey = '*************************'
	maxNumRetries = 10
	params = {'visualFeatures':'Categories,Tags,Description,Color'}
	headers = {
		'Ocp-Apim-Subscription-Key':apiKey,
		'Content-Type':'application/json'
	}
	def checkImage(self,url):
		json = {'url':url}
		data = None
		result = self.processRequest(json,data)
		returnData = {
			'category':[],
			'tags':[],
			'foreground':'',
			'background':''
		}
		if result is not None:
			for thisCategory in result['categories']:
				returnData['category'].append(thisCategory['name'])
			for thisTag in result['description']['tags']:
				returnData['tags'].append(thisTag)
			returnData['foreground'] = result['color']['dominantColorForeground']
			returnData['background'] = result['color']['dominantColorBackground']
			return returnData
		else:
			return None
	
	def processRequest(self,json,data):
		retries = 0
		result = None

		while True:
			response = requests.request('post',self.apiURL,json = json,data = data,headers = self.headers,params = self.params)
			if response.status_code == 429: 
				print("Message: %s" % (response.json()))
				if retries <= self.maxNumRetries: 
					time.sleep(5) 
					retries += 1
					continue
				else: 
					print('Error: failed after retrying!')
					break
			elif response.status_code == 200 or response.status_code == 201:
				if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
					result = None 
				elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
					if 'application/json' in response.headers['content-type'].lower(): 
						result = response.json() if response.content else None 
					elif 'image' in response.headers['content-type'].lower(): 
						result = response.content
			else:
				print("Error code: %d" % (response.status_code))
				print("Message: %s" % (response.json()))
			break
		return result

def getURLsfromCSV(csvPath):
	returnData = []
	with open(csvPath,'r') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			returnData.append(row[0])
	return returnData
	
def writeImageCSV(csvData):
	with open('imagestuff.csv', 'w', newline = '') as csvfile:
		output = csv.writer(csvfile, delimiter=',', quotechar='"')
		csvHeader = ['Image URL','Category','','','Tags','','','Foreground','Background']
		output.writerow(csvHeader)
		for thisRow in csvData:
			row = [''] * 20
			row[0] = thisRow['url']
			row[1:3] = thisRow['category'][0:3]
			row[4:6] = thisRow['tags'][0:3]
			row[7] = thisRow['foreground']
			row[8] = thisRow['background']
			output.writerow(row)

def analyzeURLsFromPath(path):
	urlData = []
	imageAPI = azureVisionAPI()
	urls = getURLsfromCSV(path)
	for index,thisURL in enumerate(urls):
		print("(",(index + 1),"/",len(urls),") Working on:",thisURL)
		imageData = imageAPI.checkImage(thisURL)
		if(imageData != None):
			thisURLData = dict()
			thisURLData['url'] = thisURL
			thisURLData['category'] = imageData['category']
			thisURLData['tags'] = imageData['tags']
			thisURLData['foreground'] = imageData['foreground']
			thisURLData['background'] = imageData['background']
			urlData.append(thisURLData)
		time.sleep(1)
	writeImageCSV(urlData)

analyzeURLsFromPath('azureimagetest.csv')
