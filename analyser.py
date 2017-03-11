import json
from pprint import pprint
import math
with open('FTP_data_all.json') as data_file:    
    data = json.load(data_file)
	
totals = [0]*11

bigtot = 0
count = 0
	
#for item in data:
#	print item['scorecard']['meta']['league']
	
factsum = 0
factsum2 = 0
	
for item in data:
#	break;
	tot1 = 0
	tot2 = 0
	if (item['scorecard']['meta']['league'].find('Pav')>-1 ):
		print item['scorecard']['meta']['league']
		if (item['scorecard']['meta']['pitch']=='Uneven'):
			MRH = float(item['ratings']['Home']['total'].replace(',',''))
			MRA = float(item['ratings']['Away']['total'].replace(',',''))
			factor = 2.0**((MRH-MRA)/(MRH+MRA))
			win = item['scorecard']['meta']['result'][:item['scorecard']['meta']['result'].find('won',0)-1]
			home =  item['scorecard']['meta']['home']
			if (win==home):
				print home, win
				factor = 1/factor
			print factor
			factsum+=factor
			factsum2 += factor*factor
			for score in item['scorecard']['scores']['In1']['bat']['scores']:
				tot1+=int(score['runs'])
			#print 'In1 ' + str(tot1)	
			count+=1
			for score in item['scorecard']['scores']['In2']['bat']['scores']:
				tot2+=int(score['runs'])
			#print 'In2 ' + str(tot2)
			count+=1
	bigtot+=tot1+tot2
print '\n'
print bigtot/count
print 2.0*factsum/count
print 2.0*factsum2/count-(2.0*factsum/count)**2


#to delete commas
# .replace(',','')