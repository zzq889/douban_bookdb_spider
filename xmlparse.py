#!/usr/bin/env python
#-*- encoding: UTF-8 -*-
from xml.dom import minidom

xmldoc = minidom.parse('book.xml')
entrys = xmldoc.getElementsByTagName('entry')

def getDoubanId(num):
	accessentry = entrys[num]
	id = accessentry.getElementsByTagName('id')[0].firstChild.data
	return id[-7:]

def getdbname(num):
	doubanid = getDoubanId(num)
	accessentry = entrys[num]
	dblist = accessentry.getElementsByTagName('db:attribute')
	dbvalue = [ i.firstChild.data for i in dblist ]
	dbname = []
	for piece in dblist:
		dbname.append(piece.attributes[piece.attributes.keys()[0]].value)
	result = zip(dbname, dbvalue)
	result.append(('doubanid', doubanid))
	return result

for i in range(10):
	print getdbname(i),
	#for j in getdbname(i):
		#print j,
	print
print '-'*60
