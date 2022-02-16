from flask import Flask, render_template, url_for, request, redirect
import nba_api
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import commonplayerinfo, teaminfocommon, teamdetails, commonteamroster
import pymongo
from pymongo import MongoClient
from django.core.paginator import Paginator
import csv
import requests
import time
from datetime import date
import http.client
import json
import random
import pyrebase
import string
import math
from observerP import NewsObserver, Observable

from info_hiding import playerFilter, teamFilter, newsFilter

#chase username and password accordingly
from observerP import createObserver

try:
    client = pymongo.MongoClient("mongodb+srv://Bibartan:bibpass@teame9db.kngdj.gcp.mongodb.net/Players?retryWrites=true&w=majority")
except:
    pass
app = Flask(__name__)

# get game information #
client = MongoClient("mongodb+srv://morganm:friedorboiled_@teame9db.kngdj.gcp.mongodb.net/GAMES?retryWrites=true&w=majority")

# firebase configuration here #
firebase_config = {
    "apiKey": "AIzaSyDdyupBP1sIkP2X4xnTrDzlvQwebsr8NKg",
    "authDomain": "ee461lteame9.firebaseapp.com",
    "databaseURL": "https://ee461lteame9.firebaseio.com",
    "projectId": "ee461lteame9",
    "storageBucket": "ee461lteame9.appspot.com",
    "messagingSenderId": "463145618553",
    "appId": "1:463145618553:web:4c18aaceaaed434f8558a8",
    "measurementId": "G-4WMNGVCXXS"
}
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth();
# config done #

# get user acc info database#
users_client = MongoClient("mongodb+srv://morganm:friedorboiled_@teame9db.kngdj.gcp.mongodb.net/Accounts?retryWrites=true&w=majority")

# create observer, observable
observable_src = Observable()
newspage = NewsObserver('NewsPage')
observable_src.register(newspage)

@app.route('/')
def root(method=['GET']):
    five_random_games = []
    five_games_info = []
    gamedb = client["GAMES"]
    gamecol = gamedb["NBA2019"]

    #get 5 random games
    for i in range(5):
       randomgame = random.randrange(1061)
       five_random_games.append(randomgame)
       game_info = []
       gamedoc = gamecol.find_one({"_id":randomgame})
       game_info.append(gamedoc["HomePoints"])
       game_info.append(gamedoc["HomeTeam"])
       game_info.append(gamedoc["AwayPoints"])
       game_info.append(gamedoc["AwayTeam"])
       five_games_info.append(game_info)

    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    currentuser = userscol.find_one({"_id":"current_user"})

    if currentuser["loggedin"]:
        # user is logged in, display logged in button
        return render_template('index.html', scores=five_games_info, log=True)
    else:
        return render_template('index.html', scores=five_games_info, log=False)


@app.route('/Players', methods=['GET', 'POST'])
def Players():
    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    currentuser = userscol.find_one({"_id":"current_user"})

    db_players = client['Players']
    collection_players = db_players['NBA_selected']
    players = []
    for document in collection_players.find():
        players.append(document)
    players = sorted(players, key=lambda k: k['Name'])

    player_filter = playerFilter(players)
    if request.method == 'GET':
        player_filter.collect_players_from_search(request.args.get('SearchCategory'), request.args.get('search'))
        player_filter.collect_players_by_name(request.args.get('Name'))
        player_filter.collect_players_by_status(request.args.get('Status'))
        player_filter.collect_players_by_position(request.args.get('Position'))
        player_filter.collect_players_by_team(request.args.get('Team'))
        player_filter.sort_players(request.args.get('Sort'))

        playersDict = {
            'players': player_filter.players,
            'filter_name': player_filter.filter_name,
            'filter_position': player_filter.filter_position,
            'filter_team': player_filter.filter_team,
            'filter_status': player_filter.filter_status,
            'search': player_filter.search,
            'search_category': player_filter.search_category,
            'sort': player_filter.sort
        }

        lastpage_range = math.ceil(len(playersDict['players'])/6)
        p = Paginator(playersDict['players'], 6) #6 entries per page
        num_pages = p.num_pages
        page = request.args.get('page', 1, type=int)
        posts = p.get_page(page).object_list
        p_range = findPageRange(page, 5, lastpage_range)
        return render_template('players.html', playersDict = playersDict, p_range=p_range, page=page, posts=posts, num_pages=num_pages, log=currentuser["loggedin"])
   
    else: 

        playersDict = {
            'players': player_filter.players,
            'filter_name': "All names",
            'filter_position': "All positions",
            'filter_team': "All teams",
            'filter_status': "All statuses",
            'search': "None",
            'search_category': "None",
            'sort': 'Default: Name (A-Z)'
        }

        lastpage_range = math.ceil(len(playersDict['players'])/6)
        p = Paginator(playersDict['players'], 6) #6 entries per page
        num_pages = p.num_pages
        page = request.args.get('page', 1, type=int)
        posts = p.get_page(page).object_list
        p_range = findPageRange(page, 5, lastpage_range)
        return render_template('players.html', playersDict = playersDict, p_range=p_range, page=page, posts=posts, num_pages=num_pages, log=currentuser["loggedin"])

@app.route('/Teams', methods=['GET', 'POST'])
def Teams():
    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    currentuser = userscol.find_one({"_id":"current_user"})

    teams = []
    db = client['Teams']
    NBA = db['NBA']
    WNBA = db['WNBA']
    for document in NBA.find():
        teams.append(document)
    for document in WNBA.find():
        teams.append(document)
    teams = sorted(teams, key=lambda k: k['Name'])
    team_filter = teamFilter(teams)

    if request.method == 'GET':
        team_filter.collect_teams_by_search(request.args.get('SearchCategory'), request.args.get('search'))
        team_filter.collect_teams_by_name(request.args.get('Name'))
        team_filter.collect_teams_by_league(request.args.get('League'))
        team_filter.collect_teams_by_conference(request.args.get('Conference'))
        team_filter.collect_teams_by_division(request.args.get('Division'))
        team_filter.sort_teams(request.args.get('Sort'))

        teamsDict = {
            'teams' : team_filter.teams,
            'filter_name' : team_filter.filter_name,
            'filter_league' : team_filter.filter_league,
            'filter_conference' : team_filter.filter_conference,
            'filter_division' : team_filter.filter_division,
            'search' : team_filter.search,
            'search_category' : team_filter.search_category,
            'sort' : team_filter.sort
        }

        p = Paginator(teamsDict['teams'], 6) #6 entries per page
        num_pages = p.num_pages
        page = request.args.get('page', 1, type=int)
        posts = p.get_page(page).object_list
        return render_template('teams.html', teamsDict = teamsDict, page=page, posts=posts, num_pages=num_pages, log=currentuser["loggedin"])
    else:

        teamsDict = {
            'teams' : team_filter.teams,
            'filter_name' : "All names",
            'filter_league' : "All leagues",
            'filter_conference' : "All conferences",
            'filter_division' : "All divisions",
            'search' : "None",
            'search_category' : "None",
            'sort' : 'Default: Team Name (A-Z)'
        }


        p = Paginator(teamsDict['teams'], 6) #6 entries per page
        num_pages = p.num_pages
        page = request.args.get('page', 1, type=int)
        posts = p.get_page(page).object_list
        return render_template('teams.html', teamsDict = teamsDict, page=page, posts=posts, num_pages=num_pages, log=currentuser["loggedin"])

@app.route('/News', methods=['GET', 'POST'])
def News():
    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    currentuser = userscol.find_one({"_id":"current_user"})

    articles = []
    db = client['News']
    NBA = db['NBA']
    for document in NBA.find():
        articles.append(document)
    articles = sorted(articles, key=lambda k: k['Updated'], reverse=True)
    news_filter = newsFilter(articles)

    if request.method == 'GET':
        news_filter.collect_articles_by_search(request.args.get('SearchCategory'), request.args.get('search'))
        news_filter.collect_articles_by_title(request.args.get('Title'))
        news_filter.collect_articles_by_category(request.args.get('Category'))
        news_filter.collect_articles_by_team(request.args.get('Team'))
        news_filter.sort_articles(request.args.get('Sort'))


        newsDict = {
            'articles': news_filter.articles,
            'num_instances': len(news_filter.articles), 
            'filter_title': news_filter.filter_title,
            'filter_category': news_filter.filter_category,
            'filter_team': news_filter.filter_team,
            'sort': news_filter.sort, 
            'search': news_filter.search, 
            'search_category': news_filter.search_category
        }


        p = Paginator(news_filter.articles, 6) #6 entries per page
        num_pages = p.num_pages
        page = request.args.get('page', 1, type=int)
        posts = p.get_page(page).object_list
        return render_template('news.html', page=page, posts=posts, num_pages=num_pages, newsDict = newsDict, log=currentuser["loggedin"])
    else:
        newsDict = {
            'articles': news_filter.articles,
            'num_instances': len(news_filter.articles), 
            'filter_title': news_filter.filter_title,
            'filter_category': "All categories",
            'filter_team': "All teams",
            'sort': "Default: Date (Latest to Earliest)", 
            'search': "None", 
            'search_category': "None"
        }
        p = Paginator(news_filter.articles, 6) #6 entries per page
        num_pages = p.num_pages
        page = request.args.get('page', 1, type=int)
        posts = p.get_page(page).object_list
        return render_template('news.html', page=page, posts=posts, num_pages=num_pages, newsDict = newsDict, log=currentuser["loggedin"])


@app.route('/AboutPage')
def AboutPage():
    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    currentuser = userscol.find_one({"_id":"current_user"})
    return render_template('about.html', log=currentuser["loggedin"])


@app.route('/PlayerInstancePage', methods=['GET', 'POST'])
def PlayerInstancePage():
    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    currentuser = userscol.find_one({"_id":"current_user"})

    if request.method == 'POST':
        selected_player = request.form['InstancePage']

        db_players = client['Players']
        collection_players = db_players['NBA_selected']

        news_articles = client['News']
        collection_news = news_articles['NBA']

        for player in collection_players.find():
            if (player['Name'] == selected_player):
                articles = []
                for artic in collection_news.find():
                    if (artic['Player'] == selected_player):
                        articles.append(artic)
                return render_template('instanceplayer.html', player=player, articles=articles, log=currentuser["loggedin"])
    return 

@app.route('/addFavPlayer', methods=['GET', 'POST'])
def addedFavoritePlayer():
    confirmation = False

    playerList = []
    db = client['Players']
    NBA = db['NBA_selected']
    WNBA = db['WNBA']
    for document in NBA.find():
        playerList.append(document)
    for document in WNBA.find():
        playerList.append(document)
    playerList = sorted(playerList, key=lambda k: k['Name'])

    playerNames = []
    for person in playerList:
        playerNames.append(person['Name'].lower())

    teamList = []
    db = client['Teams']
    NBA = db['NBA']
    WNBA = db['WNBA']
    for document in NBA.find():
        teamList.append(document)
    for document in WNBA.find():
        teamList.append(document)
    teamList = sorted(teamList, key=lambda k: k['Name'])

    usersdbpre = users_client["Accounts"]
    userscolpre = usersdbpre["Users"]
    currentuserpre = userscolpre.find_one({"_id":"current_user"})

    if request.method == 'POST':
        input = request.form['favplayerbutton']
        player = input.lower()
        # get currently logged-in user, if any #
        usersdb = users_client["Accounts"]
        userscol = usersdb["Users"]
        currentuser = userscol.find_one({"_id":"current_user"})
        if currentuser["loggedin"]:
            userUID = currentuser["user_id"]
            dbPlayers = userscol.find_one({"_id": userUID})
            playerArray = dbPlayers['favorite_players']
            new = True
            confirmation = True
            for person in playerArray:
                if player == person.lower():
                    new = False

            # got User UID of logged in user
            # now find their document and prepare to add to favorite_player array
            if new == True:
                if player in playerNames:
                    userscol.update_one({"_id":userUID}, { "$push": {"favorite_players":player.title()}})
                    return render_template('addedfavplayer.html', t=confirmation, playername=player.title(),
                                       log=currentuserpre["loggedin"])
                else:
                    message = 'This is not an existing player, please try again.'
                    link = "Favorite Players page"
                    route = "/favplayer"
                    pagename = "Favorite Players"
                    return render_template('adderror.html', t=confirmation, playername=player.title(),
                                       log=currentuserpre["loggedin"], message=message, link=link, route=route, pagename=pagename)
            else:
                message = 'You already have this player added to your Favorite Players page'
                link = "Favorite Players page"
                route = "/favplayer"
                pagename = "Favorite Players"
                return render_template('adderror.html', t=confirmation, playername=player,
                                       log=currentuserpre["loggedin"], message=message, link=link, route=route, pagename=pagename)

        else:
            confirmation = False
            message = "Please log-in in order to view or add to your Favorite Players page"
            return render_template('favplayer.html', playerList=playerList, teamList=teamList, t=confirmation,
                                   message=message, log=currentuser["loggedin"])

    message = "Please log-in in order to view or add to your Favorite Players page"
    return render_template('favplayer.html', playerList=playerList, teamList=teamList,
                           message=message)


@app.route('/removeFavPlayer', methods=['GET', 'POST'])
def removedFavoritePlayer():
    usersdbpre = users_client["Accounts"]
    userscolpre = usersdbpre["Users"]
    currentuserpre = userscolpre.find_one({"_id":"current_user"})

    confirmation = False

    if request.method == 'POST':
        player = request.form['removebutton']
        # get currently logged-in user, if any #
        usersdb = users_client["Accounts"]
        userscol = usersdb["Users"]
        currentuser = userscol.find_one({"_id":"current_user"})

        if currentuser["loggedin"]:
            userUID = currentuser["user_id"]
            # got User UID of logged in user
            # now find their document and prepare to add to favorite_player array
            dbPlayers = userscol.find_one({"_id": userUID})

            userscol.update({'_id': userUID} , { '$pull' : { 'favorite_players': player}})

            confirmation = True
        else:
            confirmation = False

    return render_template('removedfavplayer.html', t=confirmation, playername=player, log=currentuserpre["loggedin"])


@app.route('/removeFavTeam', methods=['GET', 'POST'])
def removedFavoriteTeam():
    usersdbpre = users_client["Accounts"]
    userscolpre = usersdbpre["Users"]
    currentuserpre = userscolpre.find_one({"_id":"current_user"})

    if request.method == 'POST':
        team = request.form['removebutton']
        # get currently logged-in user, if any #
        usersdb = users_client["Accounts"]
        userscol = usersdb["Users"]
        currentuser = userscol.find_one({"_id":"current_user"})
        if currentuser["loggedin"]:
            userUID = currentuser["user_id"]
            # got User UID of logged in user
            # now find their document and prepare to add to favorite_player array

            dbTeams = userscol.find_one({"_id": userUID})

            userscol.update_one({'_id': userUID}, {'$pull': {'favorite_teams': team}})

            confirmation = True
        else:
            confirmation = False

    return render_template('removedfavteam.html', t=confirmation, teamname=team, log=currentuserpre["loggedin"])

def findPageRange(cur_page, available_pages, last_page):
    pagerange = []
    if cur_page < (available_pages//2) + 1:
        pagerange.append(1)
        pagerange.append(min(available_pages+1, last_page+1))
    else:
        pagerange.append(cur_page-(available_pages//2))
        pagerange.append(min(cur_page+(available_pages//2)+1, last_page+1))
    return pagerange
    
@app.route('/TeamInstancePage', methods=['GET', 'POST'])
def TeamInstancePage():
    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    currentuser = userscol.find_one({"_id":"current_user"})

    if request.method == 'POST':
        db = client['Teams']
        NBA = db['NBA']
        WNBA = db['WNBA']

        team_ = {}
        selected_team = request.form['InstancePage']
        for team in NBA.find():
            if (team['Name'] == selected_team):
                team_ = team
        for team in WNBA.find():
            if (team['Name'] == selected_team):
                team_ = team

        roster = []
        roster_all = team_['Roster']
        roster_all = roster_all[1: -1]
        roster = roster_all.split(", ")
        roster_2 = newtest = [x[1:-1] for x in roster]


        news_articles = client['News']
        collection_news = news_articles['NBA']

        
        articles = []
        for artic in collection_news.find():
            if (artic['Team'] == selected_team):
                articles.append(artic)

        players_in_team_and_db = []
        db_players = client['Players']
        collection_players = db_players['NBA_selected']
        for player in collection_players.find():
            if (player['Team'] == selected_team):
                players_in_team_and_db.append(player['Name'])
        return render_template('instanceteam.html', team=team_, roster=roster_2, players_in_db = players_in_team_and_db, articles=articles, log=currentuser["loggedin"])
    return 


@app.route('/addFavTeam', methods=['GET', 'POST'])
def addedFavoriteTeam():

    confirmation=False

    teamList = []
    db = client['Teams']
    NBA = db['NBA']
    WNBA = db['WNBA']
    for document in NBA.find():
        teamList.append(document)
    for document in WNBA.find():
        teamList.append(document)
    teamList = sorted(teamList, key=lambda k: k['Name'])

    teamNames = []
    for group in teamList:
        teamNames.append(group['Name'].lower())

    usersdbpre = users_client["Accounts"]
    userscolpre = usersdbpre["Users"]
    currentuserpre = userscolpre.find_one({"_id": "current_user"})

    if request.method == 'POST':
        input = request.form['favteambutton']
        team = input.lower()
        # get currently logged-in user, if any #
        usersdb = users_client["Accounts"]
        userscol = usersdb["Users"]
        currentuser = userscol.find_one({"_id":"current_user"})
        if currentuser["loggedin"]:
            userUID = currentuser["user_id"]
            confirmation = True
            dbTeam = userscol.find_one({"_id": userUID})
            teamArray = dbTeam['favorite_teams']
            new = True
            # got User UID of logged in user
            # now find their document and prepare to add to favorite_teams array
            for group in teamArray:
                if group.lower() == team:
                    new = False
                # got User UID of logged in user
                # now find their document and prepare to add to favorite_player array
            if new == True:
                if team in teamNames:
                    userscol.update_one({"_id": userUID}, {"$push": {"favorite_teams": team.title()}})
                    return render_template('addedfavteam.html', t=confirmation, teamname=team.title(),
                                       log=currentuserpre["loggedin"])
                else:
                    message = 'This is not an existing team, please try again.'
                    link = "Favorite Teams page"
                    route = "/favteam"
                    pagename = "Favorite Teams"
                    return render_template('adderror.html', t=confirmation, teamname=team.title(),log=currentuserpre["loggedin"], message=message, link=link, route=route, pagename=pagename)
            else:
                message = 'You already have this team added to your Favorite Teams page.'
                link = "Favorite Teams page"
                route = "/favteam"
                pagename = "Favorite Teams"
                return render_template('adderror.html', t=confirmation, teamname=team.title(),
                                       log=currentuserpre["loggedin"], message=message, link=link, route=route, pagename=pagename)
        else:
            confirmation = False
            message = "Please log-in in order to view or add to your Favorite Teams page"
            return render_template('favteam.html', teamList=teamList, t=confirmation, message=message, log=currentuser["loggedin"])

    message = "Please log-in in order to view or add to your Favorite Teams page"
    return render_template('favteam.html', teamList=teamList, message=message, t=confirmation)

@app.route('/NewsInstancePage', methods=['GET', 'POST'])
def NewsInstancePage():
    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    currentuser = userscol.find_one({"_id":"current_user"})

    if request.method == 'POST':
        db = client['News']
        NBA = db['NBA']

        db_players = client['Players']
        collection_players = db_players['NBA_selected']
        

        selected_article = request.form['InstancePage']
        for article in NBA.find():
            if (article['Title'] == selected_article):
                players_in_db = []
                for player in collection_players.find():
                    if (player['Name'] == article['Player']):
                        players_in_db.append(player['Name'])
                return render_template('instancenews.html', article=article, players_in_db = players_in_db, log=currentuser["loggedin"])
    return 
    
@app.route('/newsInstance1', methods=['GET', 'POST'])
def newsInstance_one():
    
    return render_template('news1.html')

@app.route('/newsInstance2', methods=['GET', 'POST'])
def newsInstance_two():
    
    return render_template('news2.html')

@app.route('/newsInstance3', methods=['GET', 'POST'])
def newsInstance_three():
    
    return render_template('news3.html')

@app.route('/Year', methods=['GET', 'POST'])
def Year():
    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    currentuser = userscol.find_one({"_id":"current_user"})

    year_info_documents = []
    db_year = client['Years']
    collection_year = db_year['NBA']
    for document in collection_year.find():
        year_info_documents.append(document)
    year_info_documents = sorted(year_info_documents, key=lambda k: k['Year'],reverse=True)
    year_Was_Chosen = False

    if request.method == 'GET':
        p = Paginator(year_info_documents, 10)
        num_pages = p.num_pages
        page = request.args.get('page', 1, type=int)
        posts = p.get_page(page).object_list
        which_button = "1970"
        which_button = request.args.get('submit')

        selected_year = year_info_documents[0]
        for year in year_info_documents:
            if year['Year'] == request.args.get('year'):
                selected_year = year
                year_Was_Chosen = True
        return render_template('year.html', page=page, posts=posts, num_pages=num_pages, year_Was_Chosen=year_Was_Chosen, year=selected_year, year_info_documents=year_info_documents, log=currentuser["loggedin"])
    else:
        p = Paginator(year_info_documents, 10) #10 entries per page, will help split up by decade
        num_pages = p.num_pages
        page = request.args.get('page', 1, type=int)
        posts = p.get_page(page).object_list
        return render_template('year.html', page=page, posts=posts, num_pages=num_pages, pickDecade=True, pickYear=False, year_Was_Chosen=year_Was_Chosen, year_info_documents=year_info_documents, log=currentuser["loggedin"])

@app.route('/Franchise_Leaders', methods=['GET','POST'])
def record():
    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    currentuser = userscol.find_one({"_id":"current_user"})

    db_team = client['Teams']
    collection_team = db_team['NBA']

    db_franLeaders = client['Franchise_Leaders']
    collection_franLeaders = db_franLeaders['NBA']
    franLeaders_documents = []
    for document in collection_franLeaders.find():
        franLeaders_documents.append(document)
    franLeaders_documents = sorted(franLeaders_documents,key=lambda k: k['Team Name'])

    if request.method == 'POST':
        team_requested = request.form['Team']
        team_leader_info = collection_franLeaders.find_one({"Team Name": team_requested})

        nameArray = team_leader_info['Team Name'].split()
        team_name = nameArray[len(nameArray) - 1]

        team_info = collection_team.find_one({"Name": team_name})
        wiki_page = team_info['Wikipedia']

        return render_template('franchiseleaders.html',team_info=team_info,franLeaders_documents=franLeaders_documents,team_selected=True,team_leader_info=team_leader_info,team_name=team_name,wiki_page=wiki_page,log=currentuser["loggedin"])
    else:
        return render_template('franchiseleaders.html',franLeaders_documents=franLeaders_documents,team_selected=False,log=currentuser["loggedin"])

@app.route('/Fantasy', methods=['GET', 'POST'])
def Fantasy():
    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    currentuser = userscol.find_one({"_id":"current_user"})

    db_players = client['Players']
    collection_players = db_players['NBA_selected']
    all_players = []
    for document in collection_players.find():
        all_players.append(document)
    all_players = sorted(all_players, key=lambda k: k['Name'])



    if request.method == 'POST':
        selected_players_names = []
        selected_players_names.append(request.form['Forward'])
        selected_players_names.append(request.form['Forward-Center'])
        selected_players_names.append(request.form['Forward-Guard'])
        selected_players_names.append(request.form['Center'])
        selected_players_names.append(request.form['Guard'])

        selected_players = []
        average_PTS = 0
        average_AST = 0
        average_REB = 0
        for player in all_players:
            if player['Name'] in selected_players_names:
                selected_players.append(player)
                average_PTS += (float)(player['PTS'])
                average_AST += (float)(player['AST'])
                average_REB += (float)(player['REB'])
        average_PTS /= len(selected_players) 
        average_AST /= len(selected_players)
        average_REB /= len(selected_players)

        average_PTS = round(average_PTS, 1)
        average_AST = round(average_AST, 1)
        average_REB = round(average_REB, 1)
        return render_template('fantasy.html',all_players=all_players, team_formed=True, selected_players=selected_players, average_PTS=average_PTS, average_AST=average_AST, average_REB=average_REB, log=currentuser["loggedin"])
    else:
        return render_template('fantasy.html',all_players=all_players, team_formed = False, selected_players=[], log=currentuser["loggedin"])


@app.route('/Coaches',methods = ['GET','POST'])

def coaches():
    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    currentuser = userscol.find_one({"_id":"current_user"})

    db_coaches = client['Coaches']
    collection_coaches = db_coaches['NBA']
    coaches_documents = []
    for document in collection_coaches.find():
        coaches_documents.append(document)

    if request.method == "POST":
        coach_requested = request.form['Coach']
        coach = collection_coaches.find_one({"Coach Name": coach_requested})

        return render_template('coaches.html',coaches_documents=coaches_documents,coach_selected=True,coach=coach, log=currentuser["loggedin"])
    else:
        return render_template('coaches.html',coaches_documents=coaches_documents,coach_selected=False, log=currentuser["loggedin"])

@app.route('/Settings', methods=['GET', 'POST'])
def Settings():
    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    currentuser = userscol.find_one({"_id":"current_user"})
    return render_template('settings.html', log=currentuser["loggedin"])


@app.route('/favteam', methods=['GET', 'POST'])
def favteam():

    teamList = []
    db = client['Teams']
    NBA = db['NBA']
    WNBA = db['WNBA']
    for document in NBA.find():
        teamList.append(document)
    for document in WNBA.find():
        teamList.append(document)
    teamList = sorted(teamList, key=lambda k: k['Name'])

    favTeams = []
    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    currentuser = userscol.find_one({"_id": "current_user"})
    if currentuser["loggedin"]:
        userUID = currentuser["user_id"]
        # got User UID of logged in user
        # now find their document and prepare to add to favorite_player array
        dbTeam = userscol.find_one({"_id": userUID})
        teamArray = dbTeam['favorite_teams']
        confirmation = True
        for team in teamArray:
            for x in teamList:
                if team == x['Name']:
                    favTeams.append(x)
                    break

        favteamsroster = []
        favteamchamp = []
        for group in favTeams:
            roster_all = group['Roster']

            roster_all = roster_all[1: -1]

            roster = roster_all.split(", ")

            roster_2  = [x[1:-1] for x in roster]

            favteamsroster.append(roster_2)

            if group['League'] == "NBA":
                champ_all = group["Championships"]
                champ_all = champ_all[1: -1]
                champ = champ_all.split(", ")
                champ_2 = [x[1:-1] for x in champ]
                favteamchamp.append(champ_2)

            if group['League'] == "WNBA":
                champ_all = group["Number of Championships"]
                favteamchamp.append(champ_all)

    else:
        confirmation = False
        message = "Please log-in in order to view or add to your Favorite Teams page"
        return render_template('favteam.html', teamList=teamList, t=confirmation,
                               message=message)

    # favPlayers = [playerList[0]]
    return render_template('favteam.html', teamList=teamList, t=confirmation,
                           favTeams=favTeams, log=currentuser["loggedin"], roster=favteamsroster, champ=favteamchamp)


@app.route('/favplayer', methods=['GET', 'POST'])
def favplayer():
    playerList = []
    db = client['Players']
    NBA = db['NBA_selected']
    WNBA = db['WNBA']
    for document in NBA.find():
        playerList.append(document)
    for document in WNBA.find():
        playerList.append(document)
    playerList = sorted(playerList, key=lambda k: k['Name'])

    teamList = []
    db = client['Teams']
    NBA = db['NBA']
    WNBA = db['WNBA']
    for document in NBA.find():
        teamList.append(document)
    for document in WNBA.find():
        teamList.append(document)
    teamList = sorted(teamList, key=lambda k: k['Name'])

    favPlayers = []
    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    currentuser = userscol.find_one({"_id": "current_user"})
    if currentuser["loggedin"]:
        userUID = currentuser["user_id"]
        # got User UID of logged in user
        # now find their document and prepare to add to favorite_player array
        dbPlayers = userscol.find_one({"_id": userUID})
        playerArray = dbPlayers['favorite_players']
        confirmation = True
        for player in playerArray:
            for x in playerList:
                if player == x['Name']:
                    favPlayers.append(x)
                    break


    else:
        confirmation = False
        message="Please log-in in order to view or add to your Favorite Players page"
        return render_template('favplayer.html', playerList=playerList, teamList=teamList, t=confirmation,
                               message=message, log=currentuser["loggedin"])
    return render_template('favplayer.html', playerList=playerList, teamList=teamList, t=confirmation, favPlayers=favPlayers, log=currentuser["loggedin"])


@app.route('/Sharing')

def Sharing():

    return render_template('sharing.html')


@app.route('/comparison')

def comparison():
    playerList = []
    db = client['Players']
    NBA = db['NBA_selected']
    WNBA = db['WNBA']
    for document in NBA.find():
        playerList.append(document)
    for document in WNBA.find():
        playerList.append(document)
    playerList = sorted(playerList, key=lambda k: k['Name'])

    teamList = []
    db = client['Teams']
    NBA = db['NBA']
    WNBA = db['WNBA']
    for document in NBA.find():
        teamList.append(document)
    for document in WNBA.find():
        teamList.append(document)
    teamList = sorted(teamList, key=lambda k: k['Name'])

    comparisonPlayers = []
    comparisonTeams = []
    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    currentuser = userscol.find_one({"_id": "current_user"})
    if currentuser["loggedin"]:
        userUID = currentuser["user_id"]
        # got User UID of logged in user
        # now find their document and prepare to add to favorite_player array
        dbPlayers = userscol.find_one({"_id": userUID})

        playerArray = dbPlayers['comparison_players']
        confirmation = True
        for player in playerArray:
            for x in playerList:
                if player == x['Name']:
                    comparisonPlayers.append(x)
                    break

        teamArray = dbPlayers['comparison_teams']
        confirmation = True
        for group in teamArray:
            for y in teamList:
                if group == y['Name']:
                    comparisonTeams.append(y)
                    break

    else:
        confirmation = False
        message = "Please log-in in order to view or add to your Favorite Players page"
        return render_template('comparison.html', playerList=playerList, teamList=teamList, t=confirmation,
                               message=message, log=currentuser["loggedin"])
    return render_template('comparison.html', playerList=playerList, teamList=teamList, t=confirmation,
                           comparisonPlayers=comparisonPlayers, comparisonTeams = comparisonTeams, log=currentuser["loggedin"])


@app.route('/addCompare', methods=['GET', 'POST'])
def addCompare():
    #players
    playerList = []
    db = client['Players']
    NBA = db['NBA_selected']
    WNBA = db['WNBA']
    for document in NBA.find():
        playerList.append(document)
    for document in WNBA.find():
        playerList.append(document)
    playerList = sorted(playerList, key=lambda k: k['Name'])

    #teams
    teamList = []
    db = client['Teams']
    NBA = db['NBA']
    WNBA = db['WNBA']
    for document in NBA.find():
        teamList.append(document)
    for document in WNBA.find():
        teamList.append(document)
    teamList = sorted(teamList, key=lambda k: k['Name'])

    playerNames = []
    for person in playerList:
        playerNames.append(person['Name'])

    teamNames = []
    for group in teamList:
        teamNames.append(group['Name'])

    usersdbpre = users_client["Accounts"]
    userscolpre = usersdbpre["Users"]
    currentuserpre = userscolpre.find_one({"_id": "current_user"})

    if request.method == 'POST':
        type = ""
        player = ""
        team = ""
        if request.form['choices']:
            name = request.form['choices']

        if " " in name:
            player = name
        else:
            team = name

        usersdb = users_client["Accounts"]
        userscol = usersdb["Users"]
        currentuser = userscol.find_one({"_id": "current_user"})

        if currentuser["loggedin"]:
            userUID = currentuser["user_id"]
            db = userscol.find_one({"_id": userUID})
            #if adding a player
            if player:
                name = player
                type = "player"
                playerArray = db['comparison_players']
                new = True
                confirmation = True
                for p in playerArray:
                    if player == p:
                        new = False

            #if adding a team
            if team:
                name = team
                type = "team"
                teamArray = db['comparison_teams']
                new = True
                confirmation = True
                for group in teamArray:
                    if team == group:
                        new = False

                # got User UID of logged in user
                # now find their document and prepare to add to favorite_player array
            if new == True:
                if type:
                    if type == "player":
                        if player in playerNames:
                            userscol.update_one({"_id": userUID}, {"$push": {"comparison_players": player}})

                    if type == "team":
                        if team in teamNames:
                            userscol.update_one({"_id": userUID}, {"$push": {"comparison_teams": team}})

                    return render_template('addcompare.html', t=confirmation, name=name, type=type.upper(),
                                   log=currentuserpre["loggedin"])

                else:
                    message = 'This is not an existing' + type + ', please try again.'
                    link = "Comparisons page"
                    route = "/comparison"
                    pagename = "Comparison charts"
                    return render_template('adderror.html', t=confirmation, name=player,
                                               log=currentuserpre["loggedin"], message=message, link=link, route=route, pagename=pagename)

            else:
                    message = 'You already have this' + type + 'added to your Comparison Chart'
                    link = "Comparisons page"
                    route = "/comparison"
                    pagename = "Comparison charts"
                    return render_template('adderror.html', t=confirmation, name=name,
                                           log=currentuserpre["loggedin"], message=message, link=link, route=route, pagename=pagename)

        else:
            confirmation = False
            message = "Please log-in in order to view or add to your Comparisons page"
            return render_template('comparison.html', playerList=playerList, teamList=teamList, t=confirmation,
                                   message=message, log=currentuser["loggedin"])

    message = "Please log-in in order to view or add to your Comparisons page"
    return render_template('comparison.html', playerList=playerList, teamList=teamList,
                           message=message)





@app.route('/removeComparisonPlayer', methods=['GET', 'POST'])
def removeComparisonPlayer():
    usersdbpre = users_client["Accounts"]
    userscolpre = usersdbpre["Users"]
    currentuserpre = userscolpre.find_one({"_id": "current_user"})

    confirmation = False

    if request.method == 'POST':
        player = request.form['removebutton']
        type="PLAYER"
        # get currently logged-in user, if any #
        usersdb = users_client["Accounts"]
        userscol = usersdb["Users"]
        currentuser = userscol.find_one({"_id": "current_user"})

        if currentuser["loggedin"]:
            userUID = currentuser["user_id"]
            # got User UID of logged in user
            # now find their document and prepare to add to favorite_player array
            dbPlayers = userscol.find_one({"_id": userUID})

            userscol.update({'_id': userUID}, {'$pull': {'comparison_players': player}})

            confirmation = True
        else:
            confirmation = False

    return render_template('removecomp.html', t=confirmation, name=player, log=currentuserpre["loggedin"], type=type)


@app.route('/removeComparisonTeam', methods=['GET', 'POST'])
def removeComparisonTeam():
    usersdbpre = users_client["Accounts"]
    userscolpre = usersdbpre["Users"]
    currentuserpre = userscolpre.find_one({"_id": "current_user"})

    if request.method == 'POST':
        team = request.form['removebutton']
        type="TEAM"
        # get currently logged-in user, if any #
        usersdb = users_client["Accounts"]
        userscol = usersdb["Users"]
        currentuser = userscol.find_one({"_id": "current_user"})
        if currentuser["loggedin"]:
            userUID = currentuser["user_id"]
            # got User UID of logged in user
            # now find their document and prepare to add to favorite_player array

            dbTeams = userscol.find_one({"_id": userUID})

            userscol.update_one({'_id': userUID}, {'$pull': {'comparison_teams': team}})

            confirmation = True
        else:
            confirmation = False

    return render_template('removecomp.html', t=confirmation, name=team, log=currentuserpre["loggedin"], type=type)


@app.route('/account', methods=['GET', 'POST'])
def account():
    loggedin = 'Logged In!'
    wronginfo = 'Email/Password cannot be found!'
    if request.method == 'POST':
        email = request.form['log_email']
        password = request.form['log_pass']
        try:
            loggedin_user = auth.sign_in_with_email_and_password(email, password)
            # UPDATE the logged-in status
            usersdb = users_client["Accounts"]
            userscol = usersdb["Users"]
            currentuser = userscol.find_one({"_id": "current_user"})
            userscol.update_one({"_id":"current_user"}, { "$set": 
                {"loggedin": True, "user_id":loggedin_user['localId']}})

            return render_template('login.html', t=loggedin, log=currentuser["loggedin"])
        except:
            return render_template('login.html', f=wronginfo)
    return render_template('login.html')

@app.route('/loggedout', methods=['GET','POST'])
def loggedout():
    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    userscol.update({"_id":"current_user"}, { "$set": {"loggedin": False, "user_id":""} })

    return render_template('login.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    currentuser = userscol.find_one({"_id": "current_user"})

    created = 'Account created';
    not_created = 'Account not created, email already in use'
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        newuser = auth.create_user_with_email_and_password(email, password)
        newtoken = newuser['localId'] # <- use this to get User UID
        newuser_json = {"_id":newtoken, "email": email,
        "favorite_players": ["Ben Simmons", "Michael Jordan"], "favorite_teams": ["Rockets", "Aces"], "comparison_players":[], "comparison_teams":[], }
        userscol.insert_one(newuser_json)
        userscol.update({"_id":"current_user"}, { "$set": {"loggedin": True, "user_id":newtoken} })
        return render_template('login.html', log=currentuser["loggedin"])

    return render_template('signup.html')

@app.route('/changepassword', methods=['GET','POST'])
def changepass():
    usersdb = users_client["Accounts"]
    userscol = usersdb["Users"]
    currentuser = userscol.find_one({"_id": "current_user"})
    userUID = currentuser['user_id']
    real_user = userscol.find_one({"_id":userUID})
    auth.send_password_reset_email(real_user['email'])
    return render_template('changedpass.html', log=currentuser['loggedin'])



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)


