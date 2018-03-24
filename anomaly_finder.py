from __future__ import division
import numpy as np
import re
import matplotlib.pyplot as plt
import os
import csv
from itertools import izip
import datetime
import json


path="file.csv"
files=[]
for i in os.listdir(path):
    if os.path.isfile(os.path.join(path,i)) and 'part' in i and 'crc' not in i:
        files.append(i)


def pairwise(iterable):
	"s -> (s0, s1), (s2, s3), (s4, s5), ..."
	a = iter(iterable)
	return izip(a, a)

def get_sec(time_str):
    h, m, s = str(time_str).split(':')
    return (abs(int(h)) * 3600 + abs(int(m)) * 60 + abs(int(s)))/3600

def checkio(data,sds):
    for index in range(len(data) - 1, -1, -1):
        if data.count(data[index]) == 1:
            del data[index]
            del sds[index]
    return data,sds

time=[]
diffs=[]
date=[]
for i in range(len(files)):
	name="file.csv/"+files[i]
	spamReader = csv.reader(open(name), delimiter=' ', quotechar='|')
	c=0
	for row in spamReader:
		if len(row)!=1:
			if(row[0].split(',')[3] in date):
				c=c+1
				
			else:
				c=0
			if(c<2):
				time.append(row[1])
				date.append("".join((row[0].split(',')[3]).split("/")))
	
#print date,time
ndate,ntime=checkio(date,time)
#print ndate,ntime
format = '%H:%M:%S'
aq=[]
#print ndate[42:44],ntime[42:44]
for x, y in pairwise(ntime):
    startDateTime = datetime.datetime.strptime(x, format)
    endDateTime = datetime.datetime.strptime(y, format)
    if(startDateTime<endDateTime):
    	diff = endDateTime - startDateTime
    else:
        diff = startDateTime - endDateTime
    #print diff
    sec=get_sec(diff)
    diffs.append(float(sec))
    aq.append([float(sec),x,y])

#diffs=[10,23,12,43,54,4.23]
#print diffs

#print date
def mad(data, axis=None):
    return np.mean(np.abs(data - np.mean(data, axis)), axis)
_mad = np.abs(diffs - np.median(diffs)) / mad(diffs)
#print _mad

plt.subplot(312)
dum=np.arange(len(set(date)))
xdates=list(set(date))
print _mad
plt.xticks(dum, xdates,rotation=90)
plt.plot(dum,_mad)
#plt.xticks(range(len(_mad)), )
ano=[]
for t in _mad:
	if(t-min(_mad)>1.5):
		
		plt.annotate('Anomalous', xy=(_mad.tolist().index(t), t), xytext=(2, 6),
			    arrowprops=dict(facecolor='black', shrink=0.0005),
			    )
        ano.append(t)
adate=[]
for r in ano:
    adate.append(xdates[_mad.tolist().index(r)])
print adate
plt.savefig("/opt/lampp/htdocs/battle/statistics/num1.png",bbox_inches='tight')






