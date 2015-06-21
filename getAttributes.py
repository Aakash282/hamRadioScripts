from requests import Session
import json
import urllib2
import time 
import sys

# initialize 
input_file = str(sys.argv[1])
output_file = input_file[:-4] + '_attributes.txt'
apiHost = 'https://developer.echonest.com/api/v4/track/profile?'
tracks = [] # holds input
c = 0 # counter
keyChoice = 0
apiKey = ['5MGJPPFFJLQRSITZF', 'ULUECAILWIK1KJFED', 'VBFP0ICNRRIKKKQO6']

# load in the data
with open(input_file) as f:
	data = f.readlines()
	tracks = [str(x.strip()) for x in data]

with open(output_file) as f: 
	progress = len(f.readlines())

file_o = open(output_file, 'a')
tracks = tracks[progress:]
for t in tracks:
	c += 1
	print c
	#  5MGJPPFFJLQRSITZF ham1radioapp@gmail.com
	#  ULUECAILWIK1KJFED hamradioapp@gmail.com
	#  VBFP0ICNRRIKKKQO6 sarthak's new account
	keyChoice += 1
	keyChoice = keyChoice % 3
	URL = 'http://developer.echonest.com/api/v4/track/profile?api_key=' + api_keys[acct] + '&id=spotify:track:' + t + '&bucket=audio_summary'
	data = urllib2.urlopen(URL)
	trackSummary = json.loads(data.read())

	# Cool down before overstepping rate
	if trackSummary['response']['status']['code'] == 3:
		print "\ncooling down\n"
		time.sleep(30)

	# deal with other errors in echonest db
	elif 'track' not in trackSummary['response'].keys():
		print '\nerror skipping track\n'
		time.sleep(.5)
		continue 

	elif 'audio_summary' not in trackSummary['response']['track'].keys():
		print '\nerror skipping track\n'
		time.sleep(.5)
		continue

	elif trackSummary['response']['status']['code'] != 0:
		print '\nerror skipping track\n'
		time.sleep(.5)
		continue

	try: 
		summary = trackSummary['response']['track']['audio_summary']
	except KeyError, e: 
		print 'KeyError - missing audio_summary: %s' % str(e)
		continue

	keys = summary.keys()
	# if all keys exist then write them two the file with the id
	if keys == ['key','tempo','energy','liveness','analysis_url','speechiness','acousticness','instrumentalness','mode','time_signature','duration','loudness','valence','danceability']:
		track_sum = t + "," + str(summary['key']) + "," + str(summary['energy']) + "," + str(summary['liveness']) + "," + str(summary['tempo']) + "," + str(summary['speechiness']) + "," + str(summary['acousticness']) + "," + str(summary['instrumentalness']) + "," + str(summary['mode']) + "," + str(summary['time_signature']) + "," + str(summary['duration']) + "," + str(summary['loudness']) + "," + str(summary['valence']) + "," + str(summary['danceability']) + '\n'
		file_o.write(track_sum)
	else:
		print '\nmissing key - skipping track\n'