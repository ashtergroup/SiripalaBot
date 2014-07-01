import time , os , ConfigParser , pickle , sys , random , json , urllib2 , tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

tweet_stat = dict(mention_sl=None)
random_list =["gathering up Sri Lanka with the power in twitter",
	"Ayubowan Sri Lanka",
	"Worlds best country Sri Lanka",
	"Twitter Forever",
	"Sri Lanka, our motherland"]
config = ConfigParser.ConfigParser()
config.read('config')
w_id = "EXX0001"
auth = None
global times
times = 1

def read_stat():
	fh = open("tstat", "r")
	tweet_stat=pickle.load(fh)
def write_stat():
	fh = open("tstat", "w")
	pickle.dump(tweet_stat,fh)
def check_ban(t,u):
	if any(word in u for word in ban_user):
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
		api.update_status("The Whether in colombo looks "+ json_d["query"]["results"]["channel"]["item"]["condition"]["text"])
		print("Whether Tweet send")
	except:
		print("Whether Tweet Failed");

class TweetListner(StreamListener):
    def on_data(self, data):
		try:
			t = json.loads(data)
			if check_ban(t["text"],t["user"]["screen_name"]):
				api.retweet(t["id"])
				print("Retweeted: "+str(t["id"]))
				for ment in t["entities"]["user_mentions"]:
					if (ment["id"] == 2357666562):
						api.create_favorite(t["id"])
						print("Fevorited "+str(t["id"]))
			else:
				print("Ban "+t["user"]["screen_name"])
		except:
			print("Retweeting Failed")
		try:
			self.tim +=1
		except:
			self.tim = 1
		if self.tim<50:
			random_tweet()
		elif self.tim <55:
			whe_stat()
			self.tim = 1
		return True

    def on_error(self, status):
        print status


if __name__ == '__main__':
	TL = TweetListner()
	tweetStr = Stream(auth,TL)
	tweetStr.filter(track=["#SriLanka","#lka"])	
