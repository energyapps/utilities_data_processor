#import jsons
from urllib2 import urlopen
import simplejson as json
import time

date2 = time.strftime("%B %d, %Y")
url = 'http://api.eia.gov/series/?api_key='
APIkey = 'F6142C90B4401CFEF6C359B6BC23EBC2'

current = '{}'

crnt_master = json.loads(current)
crnt_master["dateGenerated"] = date2
crnt_master["states"] = {}
crnt_states = crnt_master["states"]

# Encode JSON into python structure
elecraw = open('electricity_meta.json')
meta_el = json.load(elecraw)

for i in range(0, len(meta_el)):
	# Call in the electricity data for each state
	series = '&series_id=' + meta_el[i]['series_id']
	FullUrl = url + APIkey + series	
	call = urlopen(FullUrl)
	data = json.load(call)	
	stateabbrev = meta_el[i]['stateabbrev']
	crnt_states[i] = {}
	crnt_states[i]['id'] = meta_el[i]['stateabbrev']
	crnt_states[i]['name'] = meta_el[i]['state']
	crnt_states[i]['data'] = data['series'][0]['data'][0][1]
	print "Successfully Added to Electricity JSON: " + meta_el[i]['state']

# Add the Date that the data is from
crnt_master["dateData"] = data['series'][0]['end']
crnt_master["source"] = 'EIA Electric Power Monthly'
crnt_master["type"] = 'Residential Utility Price (c/kWh)'

if len(crnt_master['states']) != 52:
	print "Warning: Not enough entries in Current Electricity JSON. There are only " + len(crnt_master['states']) + "entries"
else:
	print "pushed out the Electric Utility JSON from EIA"

with open('electric_utilities_monthly.json', 'wb') as f:
    json.dump(crnt_master, f)	