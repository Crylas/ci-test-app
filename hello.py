import os
import uuid
import urlparse
import redis
import json
from flask import Flask
import urllib
app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#0099FF"
GREEN = "#33CC33"
PURPLE = "#6600FF"

COLOR = PURPLE

rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
credentials = rediscloud_service['credentials']
r = redis.Redis(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])


r.set("hit_counter", 1)

@app.route('/')
def hello():
	r.incr("hit_counter")

	GetaJoke = urllib.urlopen("http://api.icndb.com/jokes/random").read()
	ParsedJoke = json.loads(GetaJoke)
	FinalJoke = str(ParsedJoke['value']['joke'])
	JokeNumber = str(ParsedJoke['value']['id'])
	
	return """
	<html>
	<body bgcolor="{}">
	<br/>
	<br/>
	<br/>
	<br/>
	
	<center><h1><font color="white">Hi, I'm a Windows PC.  Here is the GUID of the silly Python instance I am commanding: {}<br/>
	
	<br/>
	<br/>
	<br/>
	<br/>
	Random Chuck Norris Fact number {}: <br/> {} <br/>
	<br/>
	<br/>

	<font color="white"> ---> {} <--- Awesome People came here to learn about Chuck<br/></h1>
	</center>
	<br/>
	<br/>
	<br/>

	<br/>
	
	</body>
	</html>
	""".format(COLOR,my_uuid,JokeNumber,FinalJoke,r.get("hit_counter"))

	
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
