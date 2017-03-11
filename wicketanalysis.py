import json
from pprint import pprint
import math
with open('FTP_data_all.json') as data_file:    
    data = json.load(data_file)
import keys
	

seam = {'Maidens':0,'Runs':0,'Econ':0,'Count':0,'Wickets':0}
spin = {'Maidens':0,'Runs':0,'Econ':0,'Count':0,'Wickets':0}
	
pitch = 'Dry'	



for item in data:
	if (item['scorecard']['meta']['pitch']==pitch):
		
		if (item['scorecard']['scores']['In1']['ball']['scores']):
			for bowler in item['scorecard']['scores']['In1']['ball']['scores']:
				type = len(bowler['type'].split('spin',1))
				if (type == 1):
					#seam
					seam['Econ'] += float(bowler['econ'])
					seam['Runs'] += float(bowler['runs'])
					seam['Maidens'] += float(bowler['maidens'])
					seam['Wickets'] += float(bowler['wickets'])
					seam['Count'] += 1
				if (type ==2):
					#spin
					spin['Econ'] += float(bowler['econ'])
					spin['Runs'] += float(bowler['runs'])
					spin['Maidens'] += float(bowler['maidens'])
					spin['Wickets'] += float(bowler['wickets'])
					spin['Count'] +=1
					
					
		if (item['scorecard']['scores']['In2']['ball']['scores']):
			for bowler in item['scorecard']['scores']['In2']['ball']['scores']:
				type = len(bowler['type'].split('spin',1))
				if (type == 1):
					#seam
					seam['Econ'] += float(bowler['econ'])
					seam['Runs'] += float(bowler['runs'])
					seam['Maidens'] += float(bowler['maidens'])
					seam['Wickets'] += float(bowler['wickets'])
					seam['Count'] += 1
				if (type ==2):
					#spin
					spin['Econ'] += float(bowler['econ'])
					spin['Runs'] += float(bowler['runs'])
					spin['Maidens'] += float(bowler['maidens'])
					spin['Wickets'] += float(bowler['wickets'])
					spin['Count'] +=1
		

for key in seam.keys():
	if (key!='Count'):
		seam[key] = seam[key]/seam['Count']
		spin[key] = spin[key]/spin['Count']

print pitch		
print 'seam ave'
print seam
print 'spin ave' 
print spin
	