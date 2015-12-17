import urllib.request
import simplejson
import time

def get_game(iden,with_moves=False):
	"""
	get_game
		returns a game object given the lichess id
		set with_moves as true to return the moves in the game
		as a string
	"""
	query=""
	if with_moves:
		query="?with_moves=1"
	game_json=urllib.request.urlopen("http://en.lichess.org/api/game/"+iden+query).read()
	game_parsed=simplejson.loads(game_json)
	return Game(game_parsed,with_moves)

def search_games(username=None,rated=None,analysed=None,nb=100,include_moves=True):  #working: rated, nb
	"""
	search_games: queries the lichess API for a list of games
	
	parameters:
		username (optional): search only for games from this user. Don't set to search for games by any users.
		rated    (optional): 1 to find rated games, 0 to find unrated games, don't set to find any
		analysed (optional): 1 to find analyzed games, 0 to find un-analyzed games, don't set to find either
		nb       (default=100): how many results to find (the API limit seems to be around 200 but it's not consistent.
		include_moves (default=True): True if you want the query to return a list of moves in each game

	"""
	
	query="?"
	if username!=None:
		query=query+"username="+username
	if not rated==None:
		query=query+"&rated="+str(rated)
	if not analysed==None:
		query=query+"&analysed="+str(analysed)
	query=query+"&nb="+str(nb)
	if include_moves:
		query=query+"&with_moves=1"
	else:
		query=query+"&with_moves=0"	
	games_json=urllib.request.urlopen("http://en.lichess.org/api/game"+query).read()
	game_parsed=simplejson.loads(games_json)
	finalgames=[Game(each_game,include_moves) for each_game in game_parsed['list']]
	return finalgames
	
def get_user(username):
	"""
	get_user
		returns a user object
		username must be a string. it must be exact.
	"""
	current_user=urllib.request.urlopen("http://en.lichess.org/api/user/"+username).read()
	user_parsed=simplejson.loads(current_user)
	return User(user_parsed)

def search_users(team=None,nb=10):
	"""
	search_users
		use this to search for multiple users.
		nb is the number of users you want to return
		if you choose to search by team, the  doesn't take effect. Quirk of the API.
		if you do not, it will just grab nb users. Confusing. The users part of the api
		is not very useful
		team is a string, it must be the exact url
	"""
	query="nb="+str(nb)
	if not team is None:
		query=query+"&team="+team
	raw=urllib.request.urlopen("http://en.lichess.org/api/user?"+query).read()
	users_parsed=simplejson.loads(raw)
	finalreturn=[]
	if not team is None:
		finalreturn=[User(obj) for obj in users_parsed['list']]
		return finalreturn
	finalreturn=[get_user(user['username']) for user in users_parsed['list']]
	return finalreturn

class Game(object):
	"""
	class Game
		This is the "game" object.
		Most of the things down here are self explanatory. A few things:
		self.status is the way the game ended.
		self.rated is whether the game was rated or not
		self.moves returns a string of the moves in the game
	"""
	def __init__(self,raw_json,with_moves=False):
		self.keys     = raw_json.keys()

		self.id       = raw_json['id']
		self.variant  = raw_json['variant']
		self.speed    = raw_json['speed']
		self.rated    = raw_json['rated']    #Bool
		if "winner" in self.keys:
			self.winner   = raw_json['winner']   #"White" or "Black"
		self.status   = raw_json['status']   
		self.perf     = raw_json['perf']
		if "clock" in self.keys:
			self.clock    = raw_json['clock']
		self.white    = raw_json['players']['white']
		self.black    = raw_json['players']['black']
		self.url      = raw_json['url']
		self.turns    = raw_json['turns']

		if with_moves:
			self.moves=raw_json['moves']

	def __str__(self):
		return self.id


class User(object):
	"""
	class User
		This class represents the user. The objects are pretty self explanatory.
		You can do some exploration on your own--eventually I'll go back in and
		document this well.
	"""
	def __init__(self,raw_json):
		self.id       = raw_json['id']
		self.username = raw_json['username']
		self.online   = raw_json['online']
		self.engine   = raw_json['engine']
		self.booster  = raw_json['booster']
		if "language" in raw_json.keys():
			self.language = raw_json['language']
		self.profile  = raw_json['profile']
		self.url      = raw_json['url']
		self.chess960 = raw_json['perfs']['chess960']
		self.blitz    = raw_json['perfs']['blitz']
		self.threecheck = raw_json['perfs']['threeCheck']
		self.kingofthehill = raw_json['perfs']['kingOfTheHill']

	def __str__(self):
		return self.username
