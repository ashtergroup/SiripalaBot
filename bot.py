import tweepy , time , os , ConfigParser , pickle , sys , random , json , urllib2

tweet_stat = dict(mention=None,mention_sl=None,followers=None)
random_list =["gathering up Sri Lanka in twitter","Ayubowan Sri Lanka","Worlds best contry Sri Lanka","Twitter Forever"]
config = ConfigParser.ConfigParser()
config.read('config')
w_id = "EXX0001"
auth = None
times =1

def read_stat():
	fh = open("tstat", "r")
	tweet_stat=pickle.load(fh)
def write_stat():
	fh = open("tstat", "w")
	pickle.dump(tweet_stat,fh)
def check_ban(t,u):
	for i in ban_user:
		if i == u:
			return False
		else:
			if any(word in t for word in words):
				return False
			else:
				return True

try:
	auth = tweepy.OAuthHandler(config.get("Auth","a_key"),
		config.get("Auth","a_secret"))
	auth.set_access_token(config.get("Auth","a_token"),
		config.get("Auth","aa_secret"))
	words = config.get("Config","ban_words").split(' ')
	ban_user = config.get("Config","ban_user").split(' ')
except:
	print("Auth Fail")
	exit()

api = tweepy.API(auth)

if os.path.isfile("tstat"):
	print("Config found")
else:
	write_stat()

def retweet():
	read_stat()
	try:
		retweets = api.search("#SriLanka",since_id=tweet_stat["mention_sl"])
	except:
		retweets = api.search("#SriLanka")
	for t in retweets:
		try:
			if check_ban(t.text,t.user.screen_name):
				api.retweet(t.id)
				print("Retweeted: "+str(t.id))
			else:
				print("Ban "+t.user.screen_name )
		except:
			print("Retweeting Failed")
	tweet_stat["mention_sl"]=retweets[-1].id
	write_stat()

def random_tweet():
	try:
		api.update_status(random_list[random.randrange(0,len(random_list)-1)])
		print("Random Tweet Send")
	except:
		print("Random Tweet Error")

def whe_stat():
	try:
		html = urllib2.urlopen("http://query.yahooapis.com/v1/public/yql?q=select%20item%20from%20weather.forecast%20where%20location%3D%22C"+w_id+"%22&format=json")
		json_d = json.loads(html.read())
		api.update_status("The Wether in colombo looks "+ json_d["query"]["results"]["channel"]["item"]["condition"]["text"])
		print("Whether Tweet send")
	except:
		print("Whether Tweet Failed");

while True:
	if times ==6:
		random_tweet()
		times =1
	elif times == 5:
		whe_stat()
		retweet()
	retweet()
	time.sleep(10)
	print("Time out")
	time.sleep(600)
	print("Time out Over")
	times = times + 1