import json
from pprint import pprint
import math
with open('FTP_data_all.json') as data_file:    
    data = json.load(data_file)
import keys

pitch = 'Flat'	
average = [0.0]*11
partner = [0.0]*11
count = [0.0]*11

for item in data:	
	if (item['scorecard']['meta']['pitch']==pitch):
		fow_1 = keys.parsefow(item['scorecard']['scores']['In1'])
		fow_2 = keys.parsefow(item['scorecard']['scores']['In2'])
		for number in range(1,10):
			if (len(fow_1['bat']['fow'])>number-1):
				average[number] += fow_1['bat']['fow'][number-1]['score']
				partner[number] += fow_1['bat']['fow'][number-1]['score']-fow_1['bat']['fow'][number-2]['score']
				count[number] +=1
			if (len(fow_2['bat']['fow'])>number-1):
				average[number] += fow_2['bat']['fow'][number-1]['score']
				partner[number] += fow_2['bat']['fow'][number-1]['score']-fow_2['bat']['fow'][number-2]['score']
				count[number] +=1

for number in range(1,10):
	print average[number]/count[number]
	print partner[number]/count[number]
	print number