import unittest
import main

#testing CRUD (create, read, update, delete)
import pymongo
from pymongo import MongoClient

from bson import ObjectId

try:
	client = MongoClient("mongodb+srv://morganm:friedorboiled_@teame9db.kngdj.gcp.mongodb.net/GAMES?retryWrites=true&w=majority")
except:
    pass

class TestMain (unittest.TestCase):

	@classmethod
	def setUp(self):
		pass

	@classmethod
	def tearDown(self):
		pass

	#testing create account
	def test_create_account(self):

		new_account = {'_id': "new_user",
		'user_id': "00",
		'loggedin': True,
		'read_comment': 'creating new account',
		'favorite_players': [],
		'favorite_teams': []
		}

		db_accounts = client['Accounts']
		collection_accounts = db_accounts['Users']
		accounts = []
		for account in collection_accounts.find():
			accounts.append(account)

		self.assertNotIn(new_account,accounts)

		accounts.append(new_account)
		self.assertIn(new_account,accounts)

	#testing accounts collection
	def test_contains_account(self):

		db_accounts = client['Accounts']
		collection_accounts = db_accounts['Users']
		accounts = []
		for account in collection_accounts.find():
			accounts.append(account)

		account_to_find = {'_id': "RoTx9tnzNXP0Rucsxw8BVNY6O2i2",
		'email': 'newemail@gmail.com',
		'favorite_players': ['Ben Simmons', 'Michael Jordan', 'Anthony Davis', 'Carmelo Anthony'],
		'favorite_teams': ['Houston Rockets', 'Las Vegas Aces', '76ers', 'Clippers', 'Liberty', 'Dream']
		}

		self.assertIn(account_to_find,accounts)

		account_compare = collection_accounts.find_one({'email': 'newemail@gmail.com'})
		self.assertEqual(account_to_find,account_compare)

	#testing update account
	def test_update_account(self):

		db_accounts = client['Accounts']
		collection_accounts = db_accounts['Users']
		accounts = []
		for account in collection_accounts.find():
			accounts.append(account)

		account_to_update = collection_accounts.find_one({'email': 'favplayer@yahoo.com'})
		self.assertIn(account_to_update,accounts)

		account_to_update['favorite_players'].append('Lebron James')
		updated_array = account_to_update['favorite_players']
		self.assertEqual(updated_array[len(updated_array)-1],'Lebron James')
		self.assertNotIn(account_to_update,accounts)

	#testing delete account
	def test_delete_account(self):

		db_accounts = client['Accounts']
		collection_accounts = db_accounts['Users']
		accounts = []
		for account in collection_accounts.find():
			accounts.append(account)

		account_to_delete = collection_accounts.find_one({'email': 'favplayer@yahoo.com'})
		self.assertIn(account_to_delete,accounts)

		accounts.remove(account_to_delete)
		self.assertNotIn(account_to_delete,accounts)
		

	#testing create player
	def test_create_player(self):

		new_player = {'_id': '00',
		'Name': 'New Player',
		'Wikipedia': '',
		'Status': 'Active',
		'Team': 'Rockets',
		'City': 'Los Angeles',
		'Position': 'Guard',
		'Jersey': '24',
		'Height (ft)': '6.2',
		'Weight (lbs)': '180',
		'Draft Year': '2020',
		'Draft Round': '1',
		'Draft Number': '1',
		'School': 'Texas',
		'Birthday': '8/19/1999',
		'Start Year': '2020',
		'End Year': 'Present',
		'PTS': '0',
		'AST': '0',
		'REB': '0',
		'Facebook': '',
		'Instagram': '',
		'Twitter': ''}

		db_players = client['Players']
		collection_players = db_players['NBA_selected']
		players = []
		for document in collection_players.find():
			players.append(document)

		self.assertNotIn(new_player,players)

		players.append(new_player)
		self.assertIn(new_player,players)

	#testing players collection:
	def test_contains_player(self):
		
		#checking whether a player that has already been added is in the NBA_selected collection in the Players database
		db_players = client['Players']
		collection_players = db_players['NBA_selected']
		players = []
		for document in collection_players.find():
			players.append(document)
		
		player_in_db = {'_id': ObjectId('5f7ce0ba6e423c59a8ebdc4f'),
		'Name': 'Kareem Abdul-Jabbar',
		'Wikipedia': 'https://en.wikipedia.org/wiki/Kareem_Abdul-Jabbar',
		'Status': 'Not Active',
		'Team': 'Lakers',
		'City': 'Los Angeles',
		'Position': 'Center',
		'Jersey': '33',
		'Height (ft)': '7.2',
		'Weight (lbs)': '225',
		'Draft Year': '1969',
		'Draft Round': '1',
		'Draft Number': '1',
		'School': 'California-Los Angeles',
		'Birthday': '4/16/1947',
		'Start Year': '1969',
		'End Year': '1988',
		'PTS': '24.6',
		'AST': '3.6',
		'REB': '11.2',
		'Facebook': 'https://www.facebook.com/kaj',
		'Instagram': 'https://www.instagram.com/kareemabduljabbar_33/',
		'Twitter': 'https://twitter.com/kaj33',
		'reg_Blocks': 3189,
		'reg_FieldGoalsAttempted': 28307,
		'reg_FieldGoalsMade': 15837,
		'reg_FieldGoalsPercentage': 0.559472,
		'reg_FreeThrowPercentage': 0.72141,
		'reg_FreeThrowsAttempted': 9304,
		'reg_FreeThrowsMade': 6712,
		'reg_GamesPlayed': 1560,
		'reg_PersonalFouls': 4657,
		'reg_Steals': 1160,
		'reg_ThreesAttempted': 18,
		'reg_ThreesMade': 1,
		'reg_ThreesPercentage': None,
		'reg_TotalPoints': 38387,
		'reg_Turnovers': 2527
		}

		self.assertIn(player_in_db, players)
		
		search_player = collection_players.find_one({'Name': 'Kareem Abdul-Jabbar'})
		self.assertEqual(player_in_db,search_player)

	#testing update player collection
	def test_update_player(self):

		db_players = client['Players']
		collection_players = db_players['NBA_selected']
		players = []
		for document in collection_players.find():
			players.append(document)

		update_player = collection_players.find_one({'Name': 'Kevin Durant'})
		self.assertIn(update_player,players)

		update_player['PTS'] = ''
		self.assertNotIn(update_player,players)

	#testing delete player collection
	def test_delete_player(self):

		db_players = client['Players']
		collection_players = db_players['NBA_selected']
		players = []
		for document in collection_players.find():
			players.append(document)

		delete_player = collection_players.find_one({'Name': 'Kevin Durant'})
		self.assertIn(delete_player,players)

		players.remove(delete_player)
		self.assertNotIn(delete_player,players)

	#testing create coach
	def test_create_coach(self):

		db_coaches = client['Coaches']
		collections_coaches = db_coaches['NBA']
		coaches = []
		for document in collections_coaches.find():
			coaches.append(document)

		new_coach = {'_id': '0',
		'Team Name': 'Houston Rockets',
		'Coach Name': 'Bill Belichick',
		'Coach Type': 'Head Coach',
		'Season': '2020-2021'}

		self.assertNotIn(new_coach,coaches)

		coaches.append(new_coach)
		self.assertIn(new_coach,coaches)

	#testing coaches collection
	def test_contains_coach(self):

		db_coaches = client['Coaches']
		collections_coaches = db_coaches['NBA']
		coaches = []
		for document in collections_coaches.find():
			coaches.append(document)
		
		coach_to_find = {'_id': '5f7d347167193676af277fc3',
		'Location': 'Atlanta',
		'Team Name': 'Hawks',
		'Coach Name': 'Lloyd Pierce',
		'Coach Type': 'Head Coach',
		'Coaching Career Start Year': '2003',
		'Start Year with Team': '2018',
		'Wikipedia': 'https://en.wikipedia.org/wiki/Lloyd_Pierce',
		'Career Highlights as Coach': 'None',
		'Facebook': '',
		'Instagram': 'https://www.instagram.com/lp2132/',
		'Twitter': ''
		}

		self.assertIn(coach_to_find,coaches)

		search_coach = collections_coaches.find_one({'Team Name': 'Hawks'})
		self.assertEqual(coach_to_find,search_coach)

	#testing update coach
	def test_update_coach(self):

		db_coaches = client['Coaches']
		collections_coaches = db_coaches['NBA']
		coaches = []
		for document in collections_coaches.find():
			coaches.append(document)

		update_coach = collections_coaches.find_one({'Coach Name': 'Brett Brown'})
		self.assertIn(update_coach,coaches)

		update_coach['Coach Name'] = 'Doc Rivers'
		self.assertNotIn(update_coach,coaches)

	#testing delete coach
	def test_delete_coach(self):

		db_coaches = client['Coaches']
		collections_coaches = db_coaches['NBA']
		coaches = []
		for document in collections_coaches.find():
			coaches.append(document)

		delete_coach = collections_coaches.find_one({'Team Name': 'Pacers'})
		self.assertIn(delete_coach,coaches)

		coaches.remove(delete_coach)
		self.assertNotIn(delete_coach,coaches)

	#testing create news
	def test_create_news(self):

		db_news = client['News']
		collection_news = db_news['NBA']
		news = []
		for document in collection_news.find():
			news.append(document)

		new_news = {'_id': '00',
		'Updated': "2020-10-11T00:00:00",
		'Title': 'Lakers win NBA Finals',
		'Content': 'The Los Angeles Lakers have won the 2020 NBA Finals',
		'Categories': 'Risers',
		'Team': 'Lakers',
		'OriginalSource': 'Adrian Wojnarowski',
		'OrginalSourceUrl': 'https://twitter.com/wojespn',
		'Player': 'Lebron James',
		'': '34'}

		self.assertNotIn(new_news,news)

		news.append(new_news)
		self.assertIn(new_news,news)

	#testing news collection
	def test_contains_news(self):

		db_news = client['News']
		collection_news = db_news['NBA']
		news = []
		for document in collection_news.find():
			news.append(document)
		
		news_to_find = {'_id': '5fc2c34e66355c9aca3ef406',
		'Updated': '2020-10-07T01:33:45',
		'Title': 'Bam Adebayo Will Officially Return For Game 4',
		'Content': "Miami Heat center Bam  Adebayo (neck) is officially back in the starting five for Tuesday's Game 4 matchup against the Los Angeles Lakers. He has been sidelined since Game 1, so this is a big lift for Miami. It's unclear whether or not Adebayo will be limited, which makes him a risky DFS option. Kelly  Olynyk will see his minutes and playing time decrease here. Meyers  Leonard might fall out of the rotation completely.",
		'Categories': "Injuries",
		'Team': 'Heat',
		'OriginalSource': 'Tim Reynolds',
		'OriginalSourceUrl': 'https://twitter.com/ByTimReynolds/status/1313626888347291653',
		'Player': 'Bam Adebayo',
		'NewsID': "71641",
		'NewsNumber': '54'}

		self.assertIn(news_to_find,news)

		search_news = collection_news.find_one({'Title': 'Bam Adebayo Will Officially Return For Game 4'})
		self.assertEqual(news_to_find,search_news)

	#testing update news
	def test_update_news(self):

		db_news = client['News']
		collection_news = db_news['NBA']
		news = []
		for document in collection_news.find():
			news.append(document)

		update_news = collection_news.find_one({'Title': 'Doc Rivers Fired As Clippers Head Coach'})
		self.assertIn(update_news,news)

		update_news['Title'] = 'Doc Rivers Is The New Head Coach For The Philadelphia 76ers'
		update_news['Team'] = '76ers'
		self.assertNotIn(update_news,news)

	#testing delete news
	def test_delete_news(self):

		db_news = client['News']
		collection_news = db_news['NBA']
		news = []
		for document in collection_news.find():
			news.append(document)

		delete_news = collection_news.find_one({'Title': 'Marc Gasol Signing With Lakers'})
		self.assertIn(delete_news,news)

		news.remove(delete_news)
		self.assertNotIn(delete_news,news)

	#testing create franchise_leader
	def test_create_leader(self):

		db_leaders = client['Franchise_Leaders']
		collection_leaders = db_leaders['NBA']
		leaders = []
		for document in collection_leaders.find():
			leaders.append(document)

		new_leader = {'_id': '00',
		'Team Name': 'New Team',
		'Franchise Leader Points': 'New Player',
		'Total Points': '0',
		'Franchise Leader Assists': 'New Player',
		'Total Assists': '0',
		'Franchise Leader Rebounds': 'New Player',
		'Total Rebounds': '0',
		'Franchise Leader Blocks': 'New Player',
		'Total Blocks': '0',
		'Franchise Leader Steals': 'New Player',
		'Total Steals': '0'}

		self.assertNotIn(new_leader,leaders)

		leaders.append(new_leader)
		self.assertIn(new_leader,leaders)

	#testing franchise leaders collection
	def test_contains_leaders(self):

		db_leaders = client['Franchise_Leaders']
		collection_leaders = db_leaders['NBA']
		leaders = []
		for document in collection_leaders.find():
			leaders.append(document)

		leader_to_find = {'_id': ObjectId('5f7d2a2167193676af277fa5'),
		'Team Name': 'Atlanta Hawks',
		'Franchise Leader Points': 'Dominique Wilkins',
		'Total Points': '23292',
		'Franchise Leader Assists': 'Doc Rivers',
		'Total Assists': '3866',
		'Franchise Leader Rebounds': 'Bob Pettit',
		'Total Rebounds': '12849',
		'Franchise Leader Blocks': 'Tree Rollins',
		'Total Blocks': '2283',
		'Franchise Leader Steals': 'Mookie Blaylock',
		'Total Steals': '1321'}

		self.assertIn(leader_to_find,leaders)

		search_leaders = collection_leaders.find_one({'Team Name': 'Atlanta Hawks'})
		self.assertEqual(leader_to_find,search_leaders)

	#testing update leader
	def test_update_leader(self):

		db_leaders = client['Franchise_Leaders']
		collection_leaders = db_leaders['NBA']
		leaders = []
		for document in collection_leaders.find():
			leaders.append(document)

		update_leader = collection_leaders.find_one({'Team Name': 'Cleveland Cavaliers'})
		self.assertIn(update_leader,leaders)

		update_leader['BLK Franchise Leader Name'] = 'Lebron James'
		update_leader['Total Blocks'] = '1230'
		self.assertNotIn(update_leader,leaders)

	#testing delete leader
	def test_delete_leader(self):

		db_leaders = client['Franchise_Leaders']
		collection_leaders = db_leaders['NBA']
		leaders = []
		for document in collection_leaders.find():
			leaders.append(document)

		delete_leader = collection_leaders.find_one({'Team Name': 'Atlanta Hawks'})
		self.assertIn(delete_leader,leaders)

		leaders.remove(delete_leader)
		self.assertNotIn(delete_leader,leaders)

	#testing create year
	def test_create_year(self):

		db_years = client['Years']
		collections_years = db_years['NBA']
		years = []
		for document in collections_years.find():
			years.append(document)

		new_year = {'_id': '00',
		'Year': '2020',
		'Western Champion': 'Lakers',
		'Eastern Champion': 'Heat',
		'NBA Finals Winner': 'Lakers',
		'Season MVP': 'Giannis Antetokounmpo',
		'Finals MVP': 'Lebron James'}

		self.assertNotIn(new_year,years)

		years.append(new_year)
		self.assertIn(new_year,years)

	#testing years collection
	def test_contains_year(self):

		db_years = client['Years']
		collections_years = db_years['NBA']
		years = []
		for document in collections_years.find():
			years.append(document)

		years_to_find = {'_id': '5f7ae75dd9aed32f3021756c',
		'Year': '1947',
		'Western Champion': 'Warriors',
		'Eastern Champion': 'Stags',
		'NBA Finals Winner': 'Warriors',
		'Season MVP': '',
		'Finals MVP': ''}

		self.assertIn(years_to_find,years)

		search_year = collections_years.find_one({'Year': '1947'})
		self.assertEqual(years_to_find,search_year)

	#testing update year
	def test_update_year(self):

		db_years = client['Years']
		collections_years = db_years['NBA']
		years = []
		for document in collections_years.find():
			years.append(document)

		update_year = collections_years.find_one({'Year': '2016'})
		self.assertIn(update_year,years)

		update_year['NBA Finals Winner'] = 'Golden State Warriors'
		self.assertNotIn(update_year,years)

	#testing delete year
	def test_delete_year(self):

		db_years = client['Years']
		collections_years = db_years['NBA']
		years = []
		for document in collections_years.find():
			years.append(document)

		delete_year = collections_years.find_one({'Year': '1947'})
		self.assertIn(delete_year,years)

		years.remove(delete_year)
		self.assertNotIn(delete_year,years)

	#testing create game
	def test_create_game(self):

		db_games = client['GAMES']
		collection_games = db_games['NBA2019']
		games = []
		for document in collection_games.find():
			games.append(document)

		new_game = {'_id': 212,
		'HomeTeam': 'Houston Rockets',
		'HomePoints': 118,
		'AwayTeam': 'Dallas Mavericks',
		'AwayPoints': 117,
		'gameid': '00'}

		self.assertNotIn(new_game,games)

		games.append(new_game)
		self.assertIn(new_game,games)

	#testing GAMES collection
	def test_contains_games(self):

		db_games = client['GAMES']
		collection_games = db_games['NBA2019']
		games = []
		for document in collection_games.find():
			games.append(document)

		game_to_find = {'_id' : 0,
		'HomeTeam': 'Toronto Raptors',
		 'HomePoints': 130,
		'AwayTeam': 'New Orleans Pelicans',
		 'AwayPoints': 122,
		'gameid': 'c5f0698c-db24-428f-8160-52fe2b67fa08'}

		self.assertIn(game_to_find,games)

		search_game = collection_games.find_one({'gameid': 'a3f57f53-12cd-490c-831b-600be0d1041d'})
		self.assertIn(search_game,games)
		self.assertEqual(search_game['HomeTeam'],'Los Angeles Clippers')
		self.assertEqual(search_game['HomePoints'],112)
		self.assertEqual(search_game['AwayTeam'],'Los Angeles Lakers')
		self.assertEqual(search_game['AwayPoints'],102)

	#testing update game
	def test_update_game(self):

		db_games = client['GAMES']
		collection_games = db_games['NBA2019']
		games = []
		for document in collection_games.find():
			games.append(document)

		update_game = collection_games.find_one({'gameid': '12112637-31c6-4a7c-a8a3-e7468be47453'})
		self.assertEqual(update_game['HomeTeam'],'Charlotte Hornets')
		self.assertEqual(update_game['HomePoints'],126)
		self.assertEqual(update_game['AwayTeam'],'Chicago Bulls')
		self.assertEqual(update_game['AwayPoints'],125)
		self.assertIn(update_game,games)

		update_game['AwayPoints'] += 3
		self.assertEqual(update_game['AwayPoints'],128)
		self.assertNotIn(update_game,games)

	#testing delete game
	def test_delete_game(self):

		db_games = client['GAMES']
		collection_games = db_games['NBA2019']
		games = []
		for document in collection_games.find():
			games.append(document)

		delete_game = collection_games.find_one({'gameid': '9dbf6d3a-3b02-4ee8-8f41-4da4299b4f4a'})
		self.assertEqual(delete_game['HomeTeam'],'Houston Rockets')
		self.assertEqual(delete_game['HomePoints'],111)
		self.assertEqual(delete_game['AwayTeam'],'Milwaukee Bucks')
		self.assertEqual(delete_game['AwayPoints'],117)
		self.assertIn(delete_game,games)

		games.remove(delete_game)
		self.assertNotIn(delete_game,games)
	


	#testing create team
	def test_create_team(self):

		db_teams = client['Teams']
		collection_teams = db_teams['NBA']
		teams = []
		for document in collection_teams.find():
			teams.append(document)

		new_team = {'_id': '00',
		'Name': 'Supersonics',
		'League': 'NBA',
		'Location': 'Seattle',
		'Year Founded': '2020',
		'Conference': 'West',
		'Division': 'Pacific',
		'2019-2020: Wins': '0',
		'2019-2020: Losses': '0',
		'2019-2020: PCT': '0.000',
		'2019-2020: Conference Rank': '15',
		'2019-2020: Division Rank': '5',
		'Arena': 'Climate Pledge Arena',
		'Owner': 'Clay Bennett',
		'Coach': 'P.J. Carlesimo',
		'Championships': '',
		'Roster': '',
		'Facebook': '',
		'Instagram': '',
		'Twitter': '',
		'Wikipedia': ''}

		self.assertNotIn(new_team,teams)

		teams.append(new_team)
		self.assertIn(new_team,teams)

	# testing teams collection
	def test_contains_team(self):
		
		db_teams = client['Teams']
		collection_teams = db_teams['NBA']
		teams = []
		for document in collection_teams.find():
			teams.append(document)

		read_team = collection_teams.find_one({'Name': 'Celtics'})
		self.assertIn(read_team, teams)
	
		invalid_team = collection_teams.find_one({'Name': 'Texans'})
		self.assertNotIn(invalid_team, teams)

	#testing update team
	def test_update_team(self):

		db_teams = client['Teams']
		collection_teams = db_teams['NBA']
		teams = []
		for document in collection_teams.find():
			teams.append(document)

		update_team = collection_teams.find_one({'Name': 'Lakers'})
		self.assertIn(update_team,teams)

		update_team['Championships'] = "['1949 against Washington Capitols', '1950 against Syracuse Nationals (76ers)', '1952 against New York Knicks', '1953 against New York Knicks', '1954 against Syracuse Nationals (76ers)', '1972 against New York Knicks', '1980 against Philadelphia 76ers', '1982 against Philadelphia 76ers', '1985 against Boston Celtics', '1987 against Boston Celtics', '1988 against Detroit Pistons', '2000 against Indiana Pacers', '2001 against Philadelphia 76ers', '2002 against New Jersey Nets', '2009 against Orlando Magic', '2010 against Boston Celtics', '2020 against Miami Heat']"
		self.assertNotIn(update_team,teams)

	#testing delete team
	def test_delete_team(self):

		db_teams = client['Teams']
		collection_teams = db_teams['NBA']
		teams = []
		for document in collection_teams.find():
			teams.append(document)

		delete_team = collection_teams.find_one({'Name': 'Wizards'})
		self.assertIn(delete_team,teams)

		teams.remove(delete_team)
		self.assertNotIn(delete_team,teams)

	# def test_read(self):
	# 	pass
	# def test_update(self):
	# 	pass
	

if __name__ == '__main__':
	unittest.main()