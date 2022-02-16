import requests
import json
import pymongo
from pymongo import MongoClient
import time

class NewsObserver:
	def __init__(self,name):
		self.name = name

	def update(self, message):
		print('\n\nreceived News update, running update function.\n')
		# update mongoDB collection
		client = MongoClient("mongodb+srv://morganm:friedorboiled_@teame9db.kngdj.gcp.mongodb.net/News?retryWrites=true&w=majority")
		db = client["News"]
		col = db["NBA"]
		print('connected to mongoDB\n')

		for n in range(len(message['News'])):
			print('\n')
			playerID = message['News'][n]['Player']
			# translate sportradar's PlayerID to real player name
			if playerID != None:
				playersURL = 'https://api.sportsdata.io/v3/nba/scores/json/Player/'+str(playerID)+'?key=fe0b07f122f84d62beefb2c4386d2377'
				r = requests.get(url = playersURL)
				playerdata = r.json()
				message['News'][n]['Player'] = playerdata['FirstName'] + ' ' + playerdata['LastName']
			else:
				message['News'][n]['Player'] = 'FALSE'

			# translate team name abbreviation to full name
			teamID = message['News'][n]['Team']
			if teamID != None:
				message['News'][n]['Team'] = translateTeam(teamID)
			else:
				message['News'][n]['Team'] = 'No Team'

			col.insert_one(message['News'][n]) #< ----- uncomment once connected in main.py properly
			#print(message['News'][n])


class Observable:
	def __init__(self):
		self.observers = set()
		self.newsID = 0

		client = MongoClient("mongodb+srv://morganm:friedorboiled_@teame9db.kngdj.gcp.mongodb.net/News?retryWrites=true&w=majority")
		db = client["News"]
		col = db["NBA"]
		self.numberofNews = col.count()
		print(self.numberofNews)

		if col.count() == 40:
			# first time running
			getmostRecent = (col.find({}))[0]
			self.newsID = getmostRecent['NewsID']
		else:
			# not first time running 
			getmostRecent = col.find_one({'NewsNumber':str(col.count()-1)})
			self.newsID = getmostRecent['NewsID']
		print(self.newsID)
		print('created observable\n')

	def register(self, who):
		self.observers.add(who)
		print('added observer\n')

	def unregister(self, who):
		self.observers.discard(who)
		print('removed observer\n')

	def sendInfo(self, message):
		for observer in self.observers:
			print('sending info\n')
			observer.update(message) # send dict of updated News to observer.

	def checkInfo(self):
		#checks API for new information
		getNewsID = checkAPI(self.newsID)
		print('\n\n\n\n')
		print(getNewsID)
		print(self.newsID)
		if self.newsID != getNewsID:
			# initialize dict to hold new news
			newsMessage = {} # holds updated News
			newsMessage['News'] = []
			gotNewsMessage = readfromAPI(newsMessage, self.newsID, getNewsID, self.numberofNews)
			self.newsID = getNewsID # update newsID for next time
			self.numberofNews = len(gotNewsMessage['News'])
			self.sendInfo(gotNewsMessage)
		else:
			pass


def checkAPI(prev_NewsID):
	URL = 'https://api.sportsdata.io/v3/nba/scores/json/News?key=fe0b07f122f84d62beefb2c4386d2377'
	r = requests.get(url = URL)
	print('connectd to API to check\n')
	data = r.json()

	client = MongoClient("mongodb+srv://morganm:friedorboiled_@teame9db.kngdj.gcp.mongodb.net/News?retryWrites=true&w=majority")
	db = client["News"]
	col = db["NBA"]

	recent_NewsID = data[0]['NewsID']
	print(recent_NewsID)

	if col.find_one({'NewsID':recent_NewsID}) == None:
		# NewsID not found in mongo, there is News to report
		return recent_NewsID
	else:
		# no news to report
		return prev_NewsID

def readfromAPI(newsList, prev_newsID, curr_newsID, num):
	URL = 'https://api.sportsdata.io/v3/nba/scores/json/News?key=fe0b07f122f84d62beefb2c4386d2377'
	r = requests.get(url = URL)
	print('connectd to API to read\n')
	data = r.json()

	newsID_compare = curr_newsID
	counter = 0 # keep track of how many new News are being read

	while (counter < 20):
		if (data[counter]['NewsID'] == prev_newsID):
			break
		# either get most recent 20 News or until it hits the most recent newsID, whichever comes first
		newsList['News'].append({
			'NewsID': data[counter]['NewsID'],
			'Updated': data[counter]['Updated'],
			'Title': data[counter]['Title'],
			'Content': data[counter]['Content'],
			'Categories': data[counter]['Categories'],
			'Team': data[counter]['Team'],
			'OriginalSource': data[counter]['OriginalSource'],
			'OriginalSourceURL': data[counter]['OriginalSourceUrl'],
			'Player': data[counter]['PlayerID'],
			'NewsNumber': str(num)
			})
		num += 1
		counter += 1
		
	return newsList


def translateTeam(team):
	if team == 'BOS':
		return 'Celtics'
	elif team == 'BKN':
		return 'Nets'
	elif team == 'NY':
		return 'Knicks'
	elif team == 'PHI':
		return 'Sixers'
	elif team == 'TOR':
		return 'Raptors'
	elif team == 'GS':
		return 'Warriors'
	elif team == 'LAC':
		return 'Clippers'
	elif team == 'LAL':
		return 'Lakers'
	elif team == 'PHO':
		return 'Suns'
	elif team == 'SAC':
		return 'Kings'
	elif team == 'CHI':
		return 'Bulls'
	elif team == 'CLE':
		return 'Cavaliers'
	elif team == 'DET':
		return 'Pistons'
	elif team == 'IND':
		return 'Pacers'
	elif team == 'MIL':
		return 'Bucks'
	elif team == 'ATL':
		return 'Hawks'
	elif team == 'CHI':
		return 'Hornets'
	elif team == 'MIA':
		return 'Heat'
	elif team == 'ORL':
		return 'Magic'
	elif team == 'WAH':
		return 'Wizards'
	elif team == 'DEN':
		return 'Nuggets'
	elif team == 'MIN':
		return 'Timberwolves'
	elif team == 'OKC':
		return 'Thunder'
	elif team == 'POR':
		return 'TrailBlazers'
	elif team == 'UTA':
		return 'Jazz'
	elif team == 'DAL':
		return 'Mavericks'
	elif team == 'HOU':
		return 'Rockets'
	elif team == 'MEM':
		return 'Grizzlies'
	elif team == 'NO':
		return 'Pelicans'
	elif team == 'SA':
		return 'Spurs'
	else:
		return 'No Team'


# create observer and observable in main.py
# call checkInfo from main.py , news page

# remove main function once connected properly in main.py
#if __name__ == '__main__':
def createObserver():
	pub = Observable()

	newspage = NewsObserver('Page')
	pub.register(newspage)
	while True:
		pub.checkInfo()
		time.sleep(300)
		print('checking')
	print('\ndone\n')