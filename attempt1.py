import requests
import sys
import json
from BeautifulSoup import BeautifulSoup

	
def generate_data(scorecard,ratings):
	scores = generate_scorecard(scorecard);
	rating = generate_ratings(ratings);
	to_return = {'ratings':rating}
	to_return.update(scores)
	return to_return
	
def generate_scorecard(scorecard):
	total = BeautifulSoup(scorecard.content)
	raw_meta = total.findAll('table',attrs={'class':'data'})
	raw_scores = total.findAll('table',attrs={'class':'data stats marg-bottom'})
	scores = {'In1': {'bat':generate_bat(raw_scores[0]),'ball':generate_ball(raw_scores[1])},'In2': {'bat':generate_bat(raw_scores[2]),'ball':generate_ball(raw_scores[3])}}
	results = raw_meta[0]
	game_info = raw_meta[1].findAll('tr')
	if (game_info[3].td.a):
		league = game_info[3].td.a.text
		type = 'league'
	else:
		league = game_info[3].td.text
		type = 'friendly'
	meta = {'type':type,'home':game_info[0].td.a.text,'away':game_info[1].td.a.text,'league':league,'date':game_info[4].td.text,'crowd':game_info[5].td.text,'weather':game_info[6].td.span.text,'pitch':game_info[7].td.span.text,'result':raw_meta[0].tr.td.text,'toss':raw_meta[0].tr.nextSibling.nextSibling.td.text}	
	to_return = {'scores':scores, 'meta':meta}
	return to_return
	
def generate_ratings(ratings):
	total = BeautifulSoup(ratings.content)
	raw_data = total.findAll('table', attrs={'class':'data stats'})
	MRs = raw_data[0].findChildren()
	home = {'top':MRs[9].text, 'middle':MRs[13].text, 'lower': MRs[17].text, 'seam':MRs[21].text,'spin':MRs[25].text,'field':MRs[29].text,'total':MRs[33].text}
	away = {'top':MRs[10].text, 'middle':MRs[14].text, 'lower': MRs[18].text, 'seam':MRs[22].text,'spin':MRs[26].text,'field':MRs[30].text,'total':MRs[34].text}
	raw_playerranks = raw_data[1].findChildren()
	playerranks = []
	for i in range(1,23):
		player_data = raw_playerranks[5*i]
		player = {'name':player_data.td.a['title'], 'points':player_data.td.nextSibling.nextSibling.text,'mom':player_data.td.nextSibling.nextSibling.nextSibling.nextSibling.text}
		playerranks.append(player)
	to_return = {'Home':home,'Away':away,'Players':playerranks}
	return to_return
	
def generate_bat(bat):
	bat_data = {'Team Name':bat.thead.tr.th.string,'Extras':[]}
	bats = []
		
	for datum in bat.findAll('tr'):
		if (datum.th):
			if (datum.td):
				bat_data['Extras'].append(datum.td.text)
		if (datum.td):
			if (datum.td.a):
				bat = {}
				bat['long_name'] = datum.td.a['title']
				bat['short_name'] = datum.td.a.text
				wicket = datum.td.nextSibling.nextSibling
				bat['wicket'] = wicket.text
				bat['wicket2'] = ''
				bat['runs'] = 0
				bat['balls'] = 0
				bat['fours'] = 0
				bat['sixes'] = 0
				bat['sr'] = 0
				if (wicket.nextSibling.nextSibling.text):
					wicket2 =  wicket.nextSibling.nextSibling
					bat['wicket2'] = wicket2.text
					runs =  wicket2.nextSibling.nextSibling
					bat['runs'] = runs.text
					balls = runs.nextSibling.nextSibling
					bat['balls'] = balls.text
					fours = balls.nextSibling.nextSibling
					bat['fours'] = fours.text
					sixes = fours.nextSibling.nextSibling
					bat['sixes'] = sixes.text
					sr = sixes.nextSibling.nextSibling
					bat['sr'] = sr.text
				bats.append(bat)
	
	bat_data['scores'] = bats
	return bat_data

def generate_ball(ball):
	ball_data = {}
	balls = []	
	for datum in ball.findAll('tr'):
		if (datum.td):
			if (datum.td.a):
				ball = {}
				ball['long_name'] = datum.td.a['title']
				ball['short_name'] = datum.td.a.text
				ball['type'] = datum.td.span['title']
				overs = datum.td.nextSibling.nextSibling
				ball['overs'] = overs.text
				maidens = overs.nextSibling.nextSibling
				ball['maidens'] = maidens.text
				runs = maidens.nextSibling.nextSibling
				ball['runs'] = runs.text
				wickets = runs.nextSibling.nextSibling
				ball['wickets'] = wickets.text
				econ = wickets.nextSibling.nextSibling
				ball['econ'] = econ.text
				noball = econ.nextSibling.nextSibling
				ball['noball'] = noball.text
				wides = noball.nextSibling.nextSibling
				ball['wides'] = wides.text
				balls.append(ball)
	ball_data['scores'] = balls
	return ball_data


	
session = requests.session()


url1 = 'http://www.fromthepavilion.org/scorecard.htm?gameId=3818730'
login = {'j_username' :'blah1' , 'j_password' : 'vandan'}
response = session.get(url1)
html1 = response.content

url2 = 'http://www.fromthepavilion.org/securityCheck.htm'
response2 = session.post(url2, data = login)
html2 = response2.content

game_data = []

#for i in range(3818720,3818730):
for i in range(3818720,3818730):
	print i
	url_score = 'http://www.fromthepavilion.org/scorecard.htm?gameId='+str(i)
	url_ratings = 'http://www.fromthepavilion.org/ratings.htm?gameId=' + str(i)
	
	response_score = session.get(url_score)
	response_ratings = session.get(url_ratings)
	if (response_score.url != url_score or response_score.status_code==500 or response_ratings.status_code==500 or response_ratings.url!=url_ratings):
		continue
	this_data = generate_data(response_score,response_ratings)
	game_data.append(this_data)
	print len(game_data)
	
with open("FTP_data_test.json","wb") as outfile:
	json.dump(game_data,outfile)

