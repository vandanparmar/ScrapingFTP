import HTMLParser

def overparse(overs):
	split_over = overs.split('.')
	to_return =int(split_over[0])*6 + int(split_over[1][0])
	to_return = to_return / 6.0
	return to_return
	
def create_batlist(scorecard):
	list = []
	for item in scorecard['bat']['scores']:
		list.append(item['short_name'])
	return list
	
	
def parsefow(scorecard):
	score = scorecard['bat']['Extras'][2]
	bat_list = create_batlist(scorecard)	
	wicketarray = []
	for i in range(1,len(score.split('('))):
		splitter = str(i)+'-'
		this_wicket = score.split(splitter)[1]
		this_score = int(this_wicket.split(' ')[0])
		this_name = HTMLParser.HTMLParser().unescape(this_wicket.split('(')[1].split(',')[0])
		this_over = overparse(this_wicket.split(',')[1].split(')')[0])
		try: this_number = bat_list.index(this_name)+1
		except ValueError: 
			this_number = i
		wicket = {'name':this_name,'over':this_over,'wicket':i,'score':this_score,'number':this_number}
		wicketarray.append(wicket)
	scorecard['bat']['fow'] = wicketarray
	return scorecard
	print wicketarray
	
def explore(ob,n):
	if (isinstance(ob,dict)):
		for key in ob.keys():
			print key,n
			explore(ob[key],n+1)
	
	
	
#parsefow(data[0]['scores']['In1'])
#parsefow(data[0]['scores']['In2'])

#explore(data[0],0)
