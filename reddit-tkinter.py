import threading
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import praw, csv, os, datetime, time
stopwords = ["a","about","above","after","again","against","all","am","an","and","any","are","as","at","be","because","been","before","being","below","between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves" ]

class redditAPI():
	'''
	Reddit class uses PRAW to connect to Reddit/scrape comments
	API creditials can be set below
	'''
	username = "username"
	password = "password"
	clientid = "client-id"
	clientsecret = "client-secret"
	client = None
	def __init__(self,autoconnect = True):
		'''
		redditAPI object auto connects when created unless explicitly asked not to
		'''
		self.allComments = []
		self.submissionIDs = []
		self.ngrams = []
		if(autoconnect):
			self.connect()
	def connect(self):
		self.client = praw.Reddit(
			client_id = self.clientid,
			client_secret = self.clientsecret,
			password = self.password,
			user_agent = 'Reddit search data extractor by /u/{}.' . format(self.username),
			username = self.username
		)
	def search(self,keywords,subreddits):
		'''
		Loop through each subreddit and search for all keywords within that sub and get submission IDs
		Then loop through submission IDs to get actual comments
		Then create ngrams from comments
		'''
		for thisSubreddit in subreddits:
			for thisKeyword in keywords:
				self.submissionIDs.extend = [thisResult.id for thisResult in self.client.subreddit(thisSubreddit).search(thisKeyword)]
		for thisID in self.submissionIDs:
			self.allComments.extend(self.getCommentsAtSubmission(thisID))
		self.ngrams = [self.getNgrams(thisComment[0]['body']) for thisComment in self.allComments]
	def getCommentsAtSubmission(self,subID):
		'''
		Request all comments by sub ID - keeps asking for more until done (we could cap this if needed)
		Comment datatype is constructed for each comment and then returned from the function
		'''
		allComments = []
		submission = self.client.submission(subID)
		#print("Getting comments for",subID,"Comments-",submission.num_comments)
		while True:
			try:
				submission.comments.replace_more()
				#print("Getting more comments for",subID)
				break
			except PossibleExceptions:
				print('Error getting all comments',subID)
				sleep(1)
		for thisComment in submission.comments.list():
			allComments.append([{
				'id':thisComment.id,
				'subreddit':str(submission.subreddit),
				'thread':str(self.cleanUnicode(submission.title)),
				'author':str(thisComment.author),
				'body':str(self.cleanUnicode(thisComment.body)),
				'score':thisComment.score,
				'created_utc':datetime.datetime.fromtimestamp(thisComment.created_utc),
				'permalink':'http://www.reddit.com' + str(submission.permalink)
				}])
		return allComments
	def cleanUnicode(self,content):
		quotes = [[u"\u2018","'"],[u"\u2019","'"],[u"\u201c",'"'],[u"\u201d",'"']]
		for quote in quotes:
			content = content.replace(quote[0],quote[1])
		return content
	def getNgrams(self,content,maxSize = 5):
		'''
		Break content up with regex for spaces, punctuation, and symbols into individual word chunks
		Loop through all word chunks and create 2-grams, then 3-grams then maxSize grams
		ngrams can't start or end with a stop word
		'''
		global stopwords
		
		splitWords = re.split('\.|\!|\?|\(|\)|\[|\]|\{|\}|\-|\_ \'|\' | |\,|\"|\@|\#|\$|\%|\^|\&|\*|\;|\<|\>|\n|\r\n',content)
		ngrams = []
		for thisGram in splitWords:
			if thisGram != '':
				ngrams.append(thisGram.lower())
		wordCount = len(ngrams)	
		output = []		
		if(wordCount > 1):
			for strLen in range(2,maxSize):
				for start in range(wordCount - strLen + 1):
					if(ngrams[start] not in stopwords and ngrams[(start + strLen - 1)] not in stopwords):
						thisGram = " ".join(ngrams[start:(start + strLen)]).strip().lower()
						if(thisGram != ''):
							output.append(thisGram)
		return output
	def exportNGrams(self,exportPath):
		'''
		write CSV with comment ID and all ngrams
		'''
		with open(exportPath, 'w', newline = '', encoding="utf-8") as csvfile:
			output = csv.writer(csvfile, delimiter=',', quotechar='"')
			csvHeader = ['Comment ID','ngram']
			output.writerow(csvHeader)
			for thisComment in self.allComments:
				ngrams = self.getNgrams(thisComment[0]['body'])
				for thisNgram in ngrams:
					thisRow = [thisComment[0]['id'],thisNgram]
					output.writerow(thisRow)
	def exportComments(self,exportPath):
		'''
		write CSV with all comments and what sub it came from
		'''
		uniqueIDs = []
		uniqueComments = []
	
		for thisComment in self.allComments:
			if thisComment[0]['id'] not in uniqueIDs:
				uniqueIDs.append(thisComment[0]['id'])
				uniqueComments.append(thisComment)
		with open(exportPath, 'w', newline = '', encoding="utf-8") as csvfile:
			output = csv.writer(csvfile, delimiter=',', quotechar='"')
			csvHeader = []
			if len(self.allComments) > 0:
				for thisHeader in self.allComments[0][0]:
					csvHeader.append(thisHeader)
				output.writerow(csvHeader)
				for thisComment in uniqueComments:
					thisRow = []
					for thisField in thisComment[0]:
						thisRow.append(str(thisComment[0][thisField]).strip())
					output.writerow(thisRow)		

class redditScraperGUI(Tk):
	'''
	GUI class that extends TK
	'''
	saveFolderPath = None
	searchSubReddits = []
	searchTerms = []
	def __init__(self):
		'''
		Create window and frame to arrange UI elements within
		Create text variables to display messages to user_agent
		'''
		super().__init__()

		self.title("Scrape Reddit Comments")

		#add frame to self(window) to attach elenments to and layout
		frame = ttk.Frame(self, padding="3 3 12 12")
		frame.grid(column = 0, row = 0, sticky=(N, W, E, S))
		frame.columnconfigure(0, weight = 1)
		frame.rowconfigure(0, weight = 1)

		#add first row for sub reddit entry
		self.subRedditLabel = ttk.Label(frame, text = "Sub Reddits")
		self.subRedditLabel.grid(column = 1, row = 1, sticky = W)

		self.subReddits = StringVar()
		self.subRedditEntry = ttk.Entry(frame, width = 20, textvariable = self.subReddits)
		self.subRedditEntry.grid(column = 2, row = 1, sticky = (W,E))

		#add second row for search terms entry
		self.searchTermsLabel = ttk.Label(frame, text = "Search Terms")
		self.searchTermsLabel.grid(column = 1, row = 2, sticky = W)

		self.searchTerm = StringVar()
		self.searchTermsEntry = ttk.Entry(frame, width = 20, textvariable = self.searchTerm)
		self.searchTermsEntry.grid(column = 2, row = 2, sticky = (W,E))

		#add third row for folder path
		self.saveToCSVLabel = ttk.Label(frame, text = "Save CSV to")
		self.saveToCSVLabel.grid(column = 1, row = 3, sticky = W)

		self.csvPath = StringVar()
		self.csvPath.set("None")
		self.csvPathLabel = ttk.Label(frame, textvariable = self.csvPath)
		self.csvPathLabel.grid(column = 2, row = 3, sticky = (W,E))

		self.selectFolderButton = ttk.Button(frame, text = "Select Folder", command = self.selectFolder)
		self.selectFolderButton.grid(column = 3, row = 3, sticky = E)

		#add progress bar, start button, and status text
		self.currentStatus = StringVar()
		self.statusLabel = ttk.Label(frame, textvariable = self.currentStatus)
		self.statusLabel.grid(column = 2, row = 5, sticky = W)

		self.progressBar = ttk.Progressbar(frame, orient = "horizontal", length = 200, mode = "determinate")
		self.progressBar.grid(column = 2, row = 4, sticky = W)

		self.startButton = ttk.Button(frame, text = "Start", command = self.startScrape, state = 'disabled')
		self.startButton.grid(column = 3, row = 4, sticky = E)
		
		#pad everything so it looks slightly better
		for child in frame.winfo_children():
			child.grid_configure(padx=5, pady=5)
	def selectFolder(self):
		'''
		Show tkinter folder select dialog and enable start button
		'''
		self.saveFolderPath = filedialog.askdirectory()
		if(self.saveFolderPath != ''):
			self.csvPath.set(self.saveFolderPath)
			self.startButton['state'] = 'normal'
		print(self.saveFolderPath)
	def startScrape(self):
		'''
		Grab subreddit and search terms from UI (limited to 3/5)
		Call scraper handler to set up thread
		'''
		#break searches by commas		
		self.searchSubReddits = [thisSubReddit.strip().lower() for thisSubReddit in self.subRedditEntry.get().split(',')]
		self.searchTerms = [thisSearchTerm.strip().lower() for thisSearchTerm in self.searchTermsEntry.get().split(',')]
		
		if(self.searchSubReddits != [''] and self.searchTerms != ['']):
			#call scraper thread wrapper
			self.scraperHandler()
		else:
			self.currentStatus.set('Enter a sub reddit and search term')
	def scraperHandler(self):
		'''
		scraperHandler sets up the scraping function and attaches it to a separate thread so the UI can continue to run and refresh
		Actual scraper thread sets up the API class but doesn't use the search method since it can't update the UI
		Progress bar tracks how many comments have been downloaded for each subreddit and is not definitive or time-accurate
		'''
		#thread wrapper
		def scraperThread():
			#threaded process
			#since we need to update the GUI we can't use the reddit class function
			currentProgress = 0
			totalProgress = 0
			reddit = redditAPI()
			self.currentStatus.set('Finding comments...')
			
			self.progressBar['mode'] = 'indeterminate'
			self.progressBar['value'] = 0
			self.progressBar['maximum'] = 100
			self.progressBar.start(5)
			
			for thisSubreddit in self.searchSubReddits:
				subRedditExists = True
				try:
					reddit.client.subreddits.search_by_name(thisSubreddit,exact=True)
				except:
					subRedditExists = False
				if subRedditExists:
					for thisKeyword in self.searchTerms:
						reddit.submissionIDs.extend([thisResult.id for thisResult in reddit.client.subreddit(thisSubreddit).search(thisKeyword)])
				
			totalProgress += len(reddit.submissionIDs)
			self.progressBar.stop()
			self.progressBar['mode'] = 'determinate'
			self.progressBar['maximum'] = totalProgress
			
			for thisID in reddit.submissionIDs:
				reddit.allComments.extend(reddit.getCommentsAtSubmission(thisID))
				currentProgress += 1
				self.progressBar['value'] = currentProgress
				self.currentStatus.set('Thread ' + str(currentProgress) + ' of ' + str(totalProgress) + ' (' + str(len(reddit.allComments)) + ' comments)')
			self.progressBar['mode'] = 'indeterminate'
			self.progressBar['value'] = 0
			self.progressBar['maximum'] = 100
			self.progressBar.start(5)
			self.currentStatus.set('Exporting...')
			reddit.exportComments(self.saveFolderPath + "/Reddit " + " ".join(self.searchSubReddits) + " - Comments.csv")
			reddit.exportNGrams(self.saveFolderPath + "/Reddit " + " ".join(self.searchSubReddits) + " - ngrams.csv")
			
			self.currentStatus.set(str(len(reddit.allComments)) + ' Comments and ngrams exported')
			self.startButton['state'] = 'normal'
			self.progressBar['mode'] = 'determinate'
			self.progressBar.stop()
		#set up before starting thread
		self.startButton['state'] = 'disabled'
		self.currentStatus.set('')
		threading.Thread(target = scraperThread).start()

if __name__ == '__main__':
	app = redditScraperGUI()
	app.mainloop()
