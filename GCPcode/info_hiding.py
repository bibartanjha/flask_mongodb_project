import requests
import json
import pymongo
from pymongo import MongoClient
import time

class playerFilter:
    def __init__(self,players_array):
        self.players = players_array
        self.filter_name = ""
        self.filter_position = ""
        self.filter_team = ""
        self.filter_status = ""
        self.search = ""
        self.search_category = ""
        self.sort = ""

    def collect_players_from_search(self, search_category_request, search_request):
        self.search_category = search_category_request
        self.search = search_request
        if self.search_category != None and self.search_category != "None" and self.search_category != "Search Category" and self.search_category != "":
            if (self.search != None and self.search != "None" and self.search != ""):
                self.search = self.search.lower()
                players_temp = []
                for player in self.players:
                    player_attribute = player[self.search_category].lower()
                    if self.search_category == 'Status':
                        if self.search == player_attribute:
                            players_temp.append(player)
                    else:
                        if self.search in player_attribute:
                            players_temp.append(player)
                self.players = players_temp

    def collect_players_by_name(self, request_name):
        self.filter_name = request_name
        if (self.filter_name != None):
            self.filter_name = self.filter_name.lower()
            if (self.filter_name != "none" and self.filter_name != "all names"):
                players_with_name = []
                for player in self.players:
                    player_attribute = player['Name'].lower()
                    if self.filter_name in player_attribute:
                        players_with_name.append(player)
                self.players = players_with_name

    def collect_players_by_status(self, request_status):
        self.filter_status = request_status
        if (self.filter_status != None):
            self.filter_status = self.filter_status.lower()
            if (self.filter_status != "none" and self.filter_status != "all statuses" and self.filter_status != "filter by status"):
                players_with_status = []
                for player in self.players:
                    player_attribute = player['Status'].lower()
                    if self.filter_status == player_attribute:
                        players_with_status.append(player)
                self.players = players_with_status

    def collect_players_by_position(self, request_position):
        self.filter_position = request_position
        if (self.filter_position != None):
            self.filter_position = self.filter_position.lower()
            if (self.filter_position != "none" and self.filter_position != "all positions" and self.filter_position != "filter by position"):
                players_in_position = []
                for player in self.players:
                    player_attribute = player['Position'].lower()
                    if self.filter_position in player_attribute:
                        players_in_position.append(player)
                self.players = players_in_position

    def collect_players_by_team(self, request_team):
        self.filter_team = request_team 
        if (self.filter_team != None):
            self.filter_team = self.filter_team.lower()
            if (self.filter_team != "none" and self.filter_team != "all teams" and self.filter_team != "filter by team"):
                players_in_team = []
                for player in self.players:
                    player_attribute = player['Team'].lower()
                    if self.filter_team in player_attribute:
                        players_in_team.append(player)
                self.players = players_in_team

    def sort_players(self, request_sort):
        self.sort = request_sort
        if self.sort == "Name (Z-A)" or self.sort == "Sort by": 
            self.players = sorted(self.players, key=lambda k: k['Name'], reverse=True)
        elif self.sort == "Start Year (Earliest to Latest)":
            self.players = sorted(self.players, key=lambda k: k['Start Year'])
        elif self.sort == "Start Year (Latest to Earliest)":
            self.players = sorted(self.players, key=lambda k: k['Start Year'], reverse=True)
        elif self.sort == "End Year (Earliest to Latest)":
            self.players = sorted(self.players, key=lambda k: k['End Year'])
        elif self.sort == "End Year (Latest to Earliest)":
            self.players = sorted(self.players, key=lambda k: k['End Year'], reverse=True)


class teamFilter:
    def __init__(self,teams_array):
        self.teams = teams_array
        self.filter_name = ""
        self.filter_league = ""
        self.filter_conference = ""
        self.filter_division = ""
        self.which_button = ""
        self.search = ""
        self.search_category = ""
        self.sort = ""

    def collect_teams_by_search(self, request_search_category, request_search):
        self.search_category = request_search_category 
        self.search = request_search
        if self.search_category != None and self.search_category != "None" and self.search_category != "Search Category" and self.search_category != "":
            if self.search != None and self.search != "None" and self.search != "": 
                self.search = self.search.lower()
                teams_2 = []
                for team in self.teams:
                    if self.search_category == 'Division':
                        if team['League'] == 'NBA':
                            team_attribute = team[self.search_category].lower()
                            if self.search in team_attribute:
                                teams_2.append(team)
                    else:
                        team_attribute = team[self.search_category].lower()
                        if self.search in team_attribute:
                            teams_2.append(team) 
                self.teams = teams_2

    def collect_teams_by_name(self, request_name):
        self.filter_name = request_name
        if (self.filter_name != None):
            self.filter_name = self.filter_name.lower()
            if (self.filter_name != "none" and self.filter_name != "all names"):
                teams_with_name = []
                for team in self.teams:
                    team_attribute = team['Name'].lower()
                    if self.filter_name in team_attribute:
                        teams_with_name.append(team)
                self.teams = teams_with_name

    def collect_teams_by_league(self, request_league):
        self.filter_league = request_league
        if (self.filter_league != None):
            self.filter_league = self.filter_league.lower()
            if (self.filter_league != "none" and self.filter_league != "all leagues" and self.filter_league != "filter by league"):
                teams_in_league = []
                for team in self.teams:
                    team_attribute = team['League'].lower()
                    if self.filter_league == team_attribute:
                        teams_in_league.append(team)
                self.teams = teams_in_league

    def collect_teams_by_conference(self, request_conference):
        self.filter_conference = request_conference
        if (self.filter_conference != None):
            self.filter_conference = self.filter_conference.lower()
            if (self.filter_conference != "none" and self.filter_conference != "all conferences" and self.filter_conference != "filter by conference"):
                teams_in_conference = []
                for team in self.teams:
                    team_attribute = team['Conference'].lower()
                    if self.filter_conference in team_attribute:
                        teams_in_conference.append(team)
                self.teams = teams_in_conference

    def collect_teams_by_division(self, request_division):
        self.filter_division = request_division
        if (self.filter_division != None):
            self.filter_division = self.filter_division.lower()
            if (self.filter_division != "none" and self.filter_division != "all divisions" and self.filter_division != "filter by division"):
                teams_in_division = []
                for team in self.teams:
                    if team['League'] == 'NBA':
                        team_attribute = team['Division'].lower()
                        if self.filter_division in team_attribute:
                            teams_in_division.append(team)
                self.teams = teams_in_division 

    def sort_teams(self, request_sort): 
        self.sort = request_sort
        if self.sort == "Team Name (Z-A)":
            self.teams = sorted(self.teams, key=lambda k: k['Name'], reverse=True) 
        elif self.sort == "Location (A-Z)":
            self.teams = sorted(self.teams, key=lambda k: k['Location']) 
        elif self.sort == "Location (Z-A)":
            self.teams = sorted(self.teams, key=lambda k: k['Location'], reverse=True) 
        elif self.sort == "Year Founded (Earliest to Latest)":
            self.teams = sorted(self.teams, key=lambda k: k['Year Founded']) 
        elif self.sort == "Year Founded (Latest to Earliest)":
            self.teams = sorted(self.teams, key=lambda k: k['Year Founded'], reverse=True)


class newsFilter:
    def __init__(self,articles_array):
        self.articles = articles_array
        self.filter_title = ""
        self.filter_category = ""
        self.filter_team = ""
        self.search = ""
        self.search_category = ""
        self.sort = ""

    def collect_articles_by_search(self, request_search_category, request_search):
        self.search_category = request_search_category
        self.search = request_search
        if self.search_category != None and self.search_category != "None" and self.search_category != "Search Category" and self.search_category != "":
            if self.search != None and self.search != "None" and self.search != "":
                self.search = self.search.lower()
                articles_temp = []
                for art in self.articles:
                    article_attribute = art[self.search_category].lower()
                    if self.search in article_attribute:
                        articles_temp.append(art)
                self.articles = articles_temp

    def collect_articles_by_title(self, request_title):
        self.filter_title = request_title
        if (self.filter_title != None):
            self.filter_title = self.filter_title.lower()
            if (self.filter_title != "none" and self.filter_title != "all titles"):
                articles_with_title = []
                for article in self.articles:
                    article_attribute = article['Title'].lower()
                    if self.filter_title in article_attribute:
                        articles_with_title.append(article)
                self.articles = articles_with_title

    def collect_articles_by_category(self, request_category):
        self.filter_category = request_category
        if (self.filter_category != None):
            self.filter_category = self.filter_category.lower()
            if (self.filter_category != "none" and self.filter_category != "all categories" and self.filter_category != "filter by category"):
                articles_in_category = []
                for article in self.articles:
                    article_attribute = article['Categories'].lower()
                    if self.filter_category in article_attribute:
                        articles_in_category.append(article)
                self.articles = articles_in_category

    def collect_articles_by_team(self, request_team):
        self.filter_team = request_team
        if (self.filter_team != None):
            self.filter_team = self.filter_team.lower()
            if (self.filter_team != "none" and self.filter_team != "all teams" and self.filter_team != "filter by team"):
                articles_for_team = []
                for article in self.articles:
                    article_attribute = article['Team'].lower()
                    if self.filter_team in article_attribute:
                        articles_for_team.append(article)
                self.articles = articles_for_team

    def sort_articles(self, request_sort):
        self.sort = request_sort
        if self.sort == "Date (Earliest to Latest)":
            self.articles = sorted(self.articles, key=lambda k: k['Updated']) 
        elif self.sort == "Title (A to Z)":
            self.articles = sorted(self.articles, key=lambda k: k['Title']) 
        elif self.sort == "Title (Z to A)":
            self.articles = sorted(self.articles, key=lambda k: k['Title'], reverse=True) 
        elif self.sort == "Source (A to Z)":
            self.articles = sorted(self.articles, key=lambda k: k['OriginalSource']) 
        elif self.sort == "Source (Z to A)":
            self.articles = sorted(self.articles, key=lambda k: k['OriginalSource'], reverse=True)