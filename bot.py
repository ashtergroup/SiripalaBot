import tweepy , time , os , ConfigParser , pickle

tweet_stat = dict(mention=None,mention_sl=None,followers=None)
config = ConfigParser.ConfigParser()
config.read('config')
auth = None

def read_stat():
	fh = open("tstat", "rb")
	tweet_stat=pickle.load(fh)
def write_stat():
	fh = open("tstat", "wb")
	pickle.dump(tweet_stat,fh)
def check_ban(t):
	if any(word in t for word in words):
		return False
	else:
		return True
try:
	auth = tweepy.OAuthHandler(config.get("Auth","a_key"),
		config.get("Auth","a_secret"))
	auth.set_access_token(config.get("Auth","a_token"),
		config.get("Auth","aa_secret"))
	words = config.get("Auth","words").split(' ')
except:
	print("Auth Fail")
	exit()

api = tweepy.API(auth)

if os.path.isfile("tstat"):
	pass
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
			if check_ban(t.text):
				api.retweet(t.id)
				print("Retweeted: "+str(t.id))
			else:
				print("Ban")
		except:
			print("Retweeting Failed")
	tweet_stat["mention_sl"]=retweets[-1].id
	write_stat()

def mention_me():
	read_stat()
	try:
		mentions = api.mentions_timeline(since_id=tweet_stat["mention"])
	except:
		mentions = api.mentions_timeline()
	for t in mentions:
		try:
			if check_ban(t.text):
				api.update_status("@"+t.user.screen_name+" Mentioned me.")
				print("Mentioned Me: "+str(t.user.screen_name))
			else:
				print("Ban")
		except:
			print("mention me Failed")
	try:
		tweet_stat["mention"]=mentions[-1].id
	write_stat()

while True:
	retweet()
	time.sleep(10)
	mention_me()
	time.sleep(600)