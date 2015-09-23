#import jsons
from urllib2 import urlopen
import simplejson as json
import time

date = time.strftime("%y-%m-%d")
url = 'http://api.eia.gov/series/?api_key='
APIkey = 'F6142C90B4401CFEF6C359B6BC23EBC2'
fuelEconomy = 27.9 # average US Fuel economy (mpg) updated August 2015
electricEconomy = 0.326 # average electric fuel economy (kWh/mi) updated August 2015

# Note its 1170 weeks of data, or 22.5 years

master = '{}'
mstr_oil = json.loads(master)
mstr_el = json.loads(master)

current = '{}'
crnt_oil_master = json.loads(current)
crnt_oil_master["dateGenerated"] = date
crnt_oil_master["states"] = {}
crnt_oil = crnt_oil_master["states"]

crnt_el_master = json.loads(current)
crnt_el_master["dateGenerated"] = date
crnt_el_master["states"] = {}
crnt_el = crnt_el_master["states"]

crnt_combo_master = json.loads(current)
crnt_combo_master["dateGenerated"] = date
crnt_combo_master["states"] = {}
crnt_combined = crnt_combo_master["states"]

oilraw = open('oil_meta.json')
# Encode JSON into python structure
meta_oil = json.load(oilraw)
elecraw = open('electricity_meta.json')
meta_el = json.load(elecraw)

for i in range(0, len(meta_oil)):
	# Call in the oil data for each area
	series = '&series_id=' + meta_oil[i]['series_id']
	FullUrl = url + APIkey + series	
	call = urlopen(FullUrl)
	data = json.load(call)	
 	# The 'i' is what the key name of the json entry is.
	data['series'][0]['id'] = meta_oil[i]['id']
	data['series'][0]['name_id'] = meta_oil[i]['name_id']
	mstr_oil[i] = data	

	name_id	= meta_oil[i]['name_id']

	crnt_oil[name_id] = {}
	# Right now the 'i' and the 'id' are one different
	crnt_oil[name_id]['id'] = i
	crnt_oil[name_id]['name_id'] = meta_oil[i]['name_id']
	crnt_oil[name_id]['data'] = data['series'][0]['data'][0]
	print "Logged to Archive and Current Week Oil File: " + meta_oil[i]['name']

# where to save it, and what to save it as?
newFile = "oil/oilweeklyarchive-" + date + '.json'

with open(newFile, 'wb') as f:
    json.dump(mstr_oil, f)

with open('current/oil.json', 'wb') as f:
    json.dump(crnt_oil_master, f)

if len(crnt_oil_master['states']) != 19:
	print "Warning: Not enough entries in Current Oil JSON"
else:
	print "pushed out the Current Oil JSON"

for i in range(0, len(meta_el)):
	# Call in the electricity data for each state
	series = '&series_id=' + meta_el[i]['series_id']
	FullUrl = url + APIkey + series	
	call = urlopen(FullUrl)
	data = json.load(call)	
	data['series'][0]['id'] = meta_el[i]['id']
	data['series'][0]['name_id'] = meta_el[i]['stateabbrev']
	mstr_el[i] = data

	stateabbrev = meta_el[i]['stateabbrev']
	crnt_el[i] = {}

	crnt_el[i]['id'] = i
	crnt_el[i]['name_id'] = meta_el[i]['stateabbrev']
	crnt_el[i]['data'] = data['series'][0]['data'][0]
	print "Logged to Archive and Current Week Electricity File: " + meta_el[i]['state']

# where to save it, and what to save it as?
newFile = "electricity/elweeklyarchive-" + date + '.json'

with open(newFile, 'wb') as f:
    json.dump(mstr_el, f)

with open('current/el.json', 'wb') as f:
    json.dump(crnt_el_master, f)

if len(crnt_el_master['states']) != 52:
	print "Warning: Not enough entries in Current Electricity JSON"
else:
	print "pushed out the Current Electricity JSON"

# call = open('current/el.json') #for local load
# crnt_el = json.load(call)

# call = open('current/oil.json') #for local load
# crnt_oil = json.load(call)

for i in range(0, len(crnt_el)):		
	crnt_combined[i] = {}
	crnt_combined[i]['id'] = meta_el[i]['stateabbrev']
	crnt_combined[i]['name'] = meta_el[i]['state']
	crnt_combined[i]['data'] = {}
	crnt_combined[i]['data']['electricity'] = {}
	crnt_combined[i]['data']['oil'] = {}

	eldata = crnt_combined[i]['data']['electricity']
	oildata = crnt_combined[i]['data']['oil']

	# edit the string to make it just i
	eldata['date'] = crnt_el[i]['data'][0]
	eldata['price'] = crnt_el[i]['data'][1]
	egallon = (eldata['price']/100) * fuelEconomy * electricEconomy
	eldata['egallon'] = egallon

	oildata['date'] = crnt_oil["US"]['data'][0]	

	if meta_el[i]['stateabbrev'] == "MA" or meta_el[i]['stateabbrev'] == "NY" or meta_el[i]['stateabbrev'] == "FL" or meta_el[i]['stateabbrev'] == "OH" or meta_el[i]['stateabbrev'] == "TX" or meta_el[i]['stateabbrev'] == "CO" or meta_el[i]['stateabbrev'] == "CA" or meta_el[i]['stateabbrev'] == "WA" or meta_el[i]['stateabbrev'] == "MN":
		here = meta_el[i]['stateabbrev']
	else:
		if meta_el[i]['stateabbrev'] == "ME" or meta_el[i]['stateabbrev'] == "NH" or meta_el[i]['stateabbrev'] == "VT" or meta_el[i]['stateabbrev'] == "NH" or meta_el[i]['stateabbrev'] == "CT" or meta_el[i]['stateabbrev'] == "RI" :
		    here = 'NE'
		elif meta_el[i]['stateabbrev'] == "NY" or meta_el[i]['stateabbrev'] == "PA" or meta_el[i]['stateabbrev'] == "NJ" or meta_el[i]['stateabbrev'] == "DE" or meta_el[i]['stateabbrev'] == "MD" or meta_el[i]['stateabbrev'] == "DC" :
		    here = 'CAT'
		elif meta_el[i]['stateabbrev'] == "WV" or meta_el[i]['stateabbrev'] == "VA" or meta_el[i]['stateabbrev'] == "NC" or meta_el[i]['stateabbrev'] == "SC" or meta_el[i]['stateabbrev'] == "GA" :
		    here = 'LAT'
		elif meta_el[i]['stateabbrev'] == "AL" or meta_el[i]['stateabbrev'] == "MS" or meta_el[i]['stateabbrev'] == "AR" or meta_el[i]['stateabbrev'] == "LA" or meta_el[i]['stateabbrev'] == "NM" :
		    here = 'GC'
		elif meta_el[i]['stateabbrev'] == "WY" or meta_el[i]['stateabbrev'] == "MT" or meta_el[i]['stateabbrev'] == "ID" or meta_el[i]['stateabbrev'] == "UT" :
		    here = 'RM'
		elif meta_el[i]['stateabbrev'] == "OR" or meta_el[i]['stateabbrev'] == "NV" or meta_el[i]['stateabbrev'] == "AZ" or meta_el[i]['stateabbrev'] == "AK" or meta_el[i]['stateabbrev'] == "HI" :
		    here = 'WCLC'
		elif meta_el[i]['stateabbrev'] == "ND" or meta_el[i]['stateabbrev'] == "SD" or meta_el[i]['stateabbrev'] == "NE" or meta_el[i]['stateabbrev'] == "KS" or meta_el[i]['stateabbrev'] == "OK" or meta_el[i]['stateabbrev'] == "MO" or meta_el[i]['stateabbrev'] == "IA" or meta_el[i]['stateabbrev'] == "WI" or meta_el[i]['stateabbrev'] == "MI" or meta_el[i]['stateabbrev'] == "IL" or meta_el[i]['stateabbrev'] == "IN" or meta_el[i]['stateabbrev'] == "KY" or meta_el[i]['stateabbrev'] == "TN" :
		    here = 'MW'
		elif meta_el[i]['stateabbrev'] == "US" :
		    here = 'US'

	oildata['price'] = crnt_oil[here]['data'][1]
	oildata['region'] = here		
	print "Successfully Added to Combined JSON: " + meta_el[i]['state']

with open('current/combined.json', 'wb') as f:
    json.dump(crnt_combo_master, f)	

if len(crnt_combo_master['states']) != 52:
	print "Warning: Not enough entries in Combined JSON"
else:
	print "pushed out the Combined JSON"    
### Maybe here is where I push to a output.log file that everything logged!!!!






