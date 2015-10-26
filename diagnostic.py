#import libraries
# from urllib2 import urlopen
import simplejson as json
import time
import inspect
from tabulate import tabulate

def lineno():
    # """Returns the current line number in our program."""
    
    lineno = inspect.currentframe().f_back.f_lineno
    return " Error on line: " + str(lineno)

print

def sortIndex(list):
	return [i[0] for i in sorted(enumerate(list), key=lambda x:x[1])]

# Open local current file and 
call = open('electric_utilities_monthly.json') #for local load
data = json.load(call)

print 'Date diagnostic generated: ' + data['dateGenerated']
# Size of the file --- should be in XXX range

if len(data['states']) != 52:	
	print
	print '!!!!Warning: Yar beware of not enough states in data!!!!' + lineno()
	print

el_price = []
name_list = []
tabular = []

# for i in range(0, len(meta_oil)):
for x in range(0, len(data['states'])):
	o = str(x)
	cur = data['states'][o]['data']
	name_list.append(data['states'][o]['name'])
	el_price.append(cur)		
	tabular.append([name_list[x], el_price[x]])

# Electricity Prices
print
if len(el_price) != 52:	
	print '!!!Warning: Yar beware of not enough states in Electricity!!!' + lineno()
	print
print "Utility Price Statistics"
print "Date Electricity Data produced: " + data['dateData']
print "The minimum: $" + str(min(el_price)) + " c/kWh | State: " + data['states'][str(el_price.index(min(el_price)))]['name']
print "The maximum: $" + str(max(el_price)) + " c/kWh | State: " + data['states'][str(el_price.index(max(el_price)))]['name']
print "The average: $" + str(sum(el_price)/len(el_price)) + " c/kWh"
print

# Print out the tabular data
print tabulate(tabular, headers=['state','electric'], tablefmt="pipe") 
print
print "End of Diagnostic Script"
print

