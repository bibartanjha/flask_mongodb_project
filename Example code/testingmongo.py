# testing mongodb again but with APIs
from pymongo import MongoClient
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import commonplayerinfo
from pandas import DataFrame
import json

# change these three lines to your own database/collection
client = MongoClient("mongodb+srv://morganm:friedorboiled_@firstcluster.7s0jg.mongodb.net/FirstDB?retryWrites=true&w=majority")
db = client.FirstDB
collection = db["TestNBA"]


print('connected to Mongo')
while(1):
	get_player = input("Name an NBA player:\n")
	if get_player == "":
		break;
	find_player = players.find_players_by_full_name(get_player)
	#print(find_player[0]['id'])

	player_doc = {'_id': find_player[0]['id'], 
					'full_name': find_player[0]['full_name'],
					'first_name': find_player[0]['first_name'], 
					'last_name': find_player[0]['last_name'],
					'is_active': find_player[0]['is_active']}


	existing_player = collection.find_one({'_id': player_doc['_id']})
	if existing_player == None:
		collection.insert_one(player_doc)
		print("added " + get_player + "\n")
	else:
		print(existing_player)
		print(get_player + " has already been added" + " \n")