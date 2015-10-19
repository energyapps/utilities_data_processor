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
call = open('current/combined.json') #for local load
data = json.load(call)

print 'Date diagnostic generated: ' + data['dateGenerated']
# Size of the file --- should be in XXX range

if len(data['states']) != 52:	
	print
	print '!!!!Warning: Yar beware of not enough states in data!!!!' + lineno()
	print

# Can I call it from the server? 

oil_price = []
el_price = []
name_list = []
diff = []
tabular = []

# for i in range(0, len(meta_oil)):
for x in range(0, len(data['states'])):
	o = str(x)
	cur = data['states'][o]['data']
	name_list.append(data['states'][o]['name'])
	oil_price.append(cur['oil']['price'])
	el_price.append(cur['electricity']['egallon'])
	diff.append(oil_price[x] - el_price[x])
	if oil_price[x] < 1:
		print "!!!!Warning there are oil values below $1 in " + data['states'][o]['name'] + ": " + str(cur['oil']['price']) + "!!!" + lineno()
		print
	if el_price[x] < 0.5:
		print "!!!!Warning there are egallon values below $0.5 in " + data['states'][o]['name'] + ": " + str(cur['electricity']['egallon'])+ "!!!" + lineno()
		print
	tabular.append([name_list[x], oil_price[x], el_price[x], diff[x]])

# Oil Prices
#  Date of records
#  High + state
#  Low + state
#  Average
print
if len(oil_price) != 52:	
	print '!!!Warning: Yar beware of not enough states in Oil!!!!!' + lineno()
	print
print "Oil Price Statistics"
print "Date Oil Data produced: " + data['states']['0']['data']['oil']['date']
print "The minimum: $" + str(min(oil_price)) + " | Region: " + data['states'][str(oil_price.index(min(oil_price)))]['data']['oil']['region']
print "The maximum: $" + str(max(oil_price)) + " | Region: " + data['states'][str(oil_price.index(max(oil_price)))]['data']['oil']['region']
print "The average: $" + str(sum(oil_price)/len(oil_price))

# Electricity Prices
#  Date of records
#  High
#  Low
#  Average
print
if len(el_price) != 52:	
	print '!!!Warning: Yar beware of not enough states in Electricity!!!' + lineno()
	print
print "Egallon Price Statistics"
print "Date Electricity Data produced: " + data['states']['0']['data']['electricity']['date']
print "The minimum: $" + str(min(el_price)) + " | State: " + data['states'][str(el_price.index(min(el_price)))]['name']
print "The maximum: $" + str(max(el_price)) + " | State: " + data['states'][str(el_price.index(max(el_price)))]['name']
print "The average: $" + str(sum(el_price)/len(el_price))
print

print 'Differences'
diffIndexSorted = sortIndex(diff)
print '3 Smallest differences in Egallon and Oil Prices'
print "1) " + data['states'][str(diffIndexSorted[0])]['name'] + ": $" + str(diff[diffIndexSorted[0]])
print "2) " + data['states'][str(diffIndexSorted[1])]['name'] + ": $" + str(diff[diffIndexSorted[1]])
print "3) " + data['states'][str(diffIndexSorted[2])]['name'] + ": $" + str(diff[diffIndexSorted[2]])
print 
print '3 Largest differences in Egallon and Oil Prices'
print "1) " + data['states'][str(diffIndexSorted[51])]['name'] + ": $" + str(diff[diffIndexSorted[51]])
print "2) " + data['states'][str(diffIndexSorted[50])]['name'] + ": $" + str(diff[diffIndexSorted[50]])
print "3) " + data['states'][str(diffIndexSorted[49])]['name'] + ": $" + str(diff[diffIndexSorted[49]])
print
print "The average difference between oil price and egallon price: $" + str(sum(diff)/len(diff)) 

# Print out the tabular data
print tabulate(tabular, headers=['state','oil','egallon','diff'], tablefmt="pipe") 
print
print "End of Diagnostic Script"
print

