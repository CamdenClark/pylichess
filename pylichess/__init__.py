import urllib.request
import simplejson
import time

def get_user(username):
	current_user=urllib.request.urlopen("http://en.lichess.org/api/user/"+username).read()
	user_parsed=simplejson.loads(current_user)
	return User(user_parsed)

def search_users(team=None,nb=10):
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
	
class User(object):
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
#k=search_users(team="coders",nb=100)
#finalk=[t.blitz['rating'] for t in k if t.blitz['rating']!=1500]
#print(finalk)

