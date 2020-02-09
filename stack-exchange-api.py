import requests, json, csv, time, re, math

class stackAPI():
	site = ''
	apiKey = '****************************'
	pageSize = 100
	maxPages = 10
	questions = []
	answers = []
	questionIDs = []
	answerIDs = []
	tags = []
	def stackExchange(self,site,query = ''):
		self.site = site
		
		if query == '':
			self.getQuestions(self.site)
		else:
			self.search(self.site,query)
		
		questionRange = math.floor(len(self.questionIDs)/100)
		for i in range(0,questionRange):
			self.getAnswersFromQuestion(self.site,";".join([str(thisID) for thisID in self.questionIDs[i * 100:(i* 100) + 100]]))
		
		answerRange = math.floor(len(self.questionIDs)/100)
		for i in range(0,answerRange):
			self.getAnswers(self.site,";".join([str(thisID) for thisID in self.answerIDs[i * 100:(i* 100) + 100]]))

	def search(self,site,query):
		apiEndpoint = 'https://api.stackexchange.com/2.2/'
		action = 'search'
	
		getData = True
		returnData = []
		allTags = {}
		page = 1
		while getData:
			config = {
				'key':self.apiKey,
				'order':'desc',
				'sort':'activity',
				'site':site,
				'intitle':query,
				'page':page,
				'pagesize':self.pageSize
			}
			HTTPrequest = requests.get(apiEndpoint + action, params = config)
			apiData = json.loads(HTTPrequest.text)
			if 'items' in apiData:
				returnData.extend(apiData['items'])
				getData = apiData['has_more']
				page = page + 1
				if(page > self.maxPages):
					break
			else:
				print(apiData)
				break
			if(getData):
				time.sleep(1)
		
		for thisQuestion in returnData:
			self.questions.append(thisQuestion)
			self.questionIDs.append(thisQuestion['question_id'])
		
		for thisQuestion in returnData:
			for thisTag in thisQuestion['tags']:
				if thisTag not in allTags:
					allTags[thisTag] = 1
				else:
					allTags[thisTag] = allTags[thisTag] + 1
		sortedTags = []
		for tagName,tagIndex in enumerate(allTags):
			sortedTags.append((allTags[tagIndex],tagIndex))
		sortedTags.sort(reverse = True)
		for thisTag in sortedTags[:100]:
			self.tags.append(thisTag[1])
	def getQuestions(self,site):
		apiEndpoint = 'https://api.stackexchange.com/2.2/'
		action = 'questions'
	
		getData = True
		returnData = []
		allTags = {}
		page = 1
		while getData:
			config = {
				'key':self.apiKey,
				'order':'desc',
				'sort':'activity',
				'site':site,
				'page':page,
				'pagesize':self.pageSize
			}
			HTTPrequest = requests.get(apiEndpoint + action, params = config)
			apiData = json.loads(HTTPrequest.text)
			if 'items' in apiData:
				returnData.extend(apiData['items'])
				getData = apiData['has_more']
				page = page + 1
				if(page > self.maxPages):
					break
			else:
				print(apiData)
				break
			if(getData):
				time.sleep(1)
		
		for thisQuestion in returnData:
			self.questions.append(thisQuestion)
			self.questionIDs.append(thisQuestion['question_id'])
		
		for thisQuestion in returnData:
			for thisTag in thisQuestion['tags']:
				if thisTag not in allTags:
					allTags[thisTag] = 1
				else:
					allTags[thisTag] = allTags[thisTag] + 1
		sortedTags = []
		for tagName,tagIndex in enumerate(allTags):
			sortedTags.append((allTags[tagIndex],tagIndex))
		sortedTags.sort(reverse = True)
		for thisTag in sortedTags[:100]:
			self.tags.append(thisTag[1])
			
	def getAnswersFromQuestion(self,site,questionID):
		apiEndpoint = 'https://api.stackexchange.com/2.2/'
		action = 'questions/' + str(questionID) + "/answers"
	
		getData = True
		returnData = []
		answerIDs = []
		page = 1
		while getData:		
			config = {
				'key':self.apiKey,
				'order':'desc',
				'sort':'activity',
				'site':site,
				'page':page,
				'pagesize':self.pageSize
			}
			HTTPrequest = requests.get(apiEndpoint + action, params = config)
			apiData = json.loads(HTTPrequest.text)
			if 'items' in apiData:
				returnData.extend(apiData['items'])
				getData = apiData['has_more']
				page = page + 1
				if(page > self.maxPages):
					break
			else:
				print(apiData)
				break
			if(getData):
				time.sleep(1)
		
		for thisAnswer in returnData:
			self.answerIDs.append(thisAnswer['answer_id'])
			
	def getAnswers(self,site,answerID):
		apiEndpoint = 'https://api.stackexchange.com/2.2/'
		action = 'answers/' + str(answerID)
	
		getData = True
		returnData = []
		page = 1
		while getData:		
			config = {
				'key':self.apiKey,
				'order':'desc',
				'sort':'activity',
				'site':site,
				'page':page,
				'pagesize':self.pageSize,
				'filter':'withbody'
			}
			HTTPrequest = requests.get(apiEndpoint + action, params = config)
			apiData = json.loads(HTTPrequest.text)
			if 'items' in apiData:
				returnData.extend(apiData['items'])
				getData = apiData['has_more']
				page = page + 1
				if(page > self.maxPages):
					break
			else:
				print(apiData)
				break
			if(getData):
				time.sleep(1)
		
		for thisAnswer in returnData:
			self.answers.append(thisAnswer)


stack = stackAPI()
stack.stackExchange('python','api')
