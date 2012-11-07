#!/usr/bin/env python
#-*- encoding: UTF-8 -*-
# fetch book data from douban with api
import urllib
import re
import linecache
import sqlite3
import time
from xml.dom import minidom

def getWebPageContent(url):
	f = urllib.urlopen(url)
	data = f.read()
	f.close()
	return data

def fetchURL(url):
	urllib.urlretrieve(url, 'book.xml')

booktags = 'python'
startIndex = 1
maxResults = 20
apikey = '0fa99d42b6d00bbb2efcd7c824702331'
url = 'http://api.douban.com/book/subjects?tag=' + booktags \
	+ '&start-index=' + str(startIndex) \
	+ '&max-results=' + str(maxResults) \
	+ 'apikey={' + apikey + '}'
#GET xml
#content = getWebPageContent(url)
fetchURL(url)
content = open('book.xml','rb').read()

#filter
result1 = re.findall(r'<entry.+?</entry', content, re.S)
result2 = re.compile(r'<db.+?</db', re.S)
rule_id = re.compile(r'subject/(.+?)</id>', re.S)
rule_title = re.compile(r'<title>(.+?)</title>', re.S)
rule_img = re.compile(r'/spic/(.+?)"', re.S)
rule_name = re.compile(r'<db:attribute name="(.+?)"', re.S)
rule_db = re.compile(r'">(.+?)</db', re.S)
result = []
for i in result1:
	#for each entry:
	piece = {}
	piece['doubanid'] = rule_id.search(i).group(1)
	#piece['doubanid'] = xmldoc.getElementsByTagName('id')[row_num].firstChild.data
	piece['title'] = rule_title.search(i).group(1)
	piece['img'] = rule_img.search(i).group(1)
	for db_piece in result2.findall(i):
		dbname = rule_name.search(db_piece).group(1)
		#creat list for author and translator
		if dbname != 'author' and dbname != 'translator':
			piece[dbname] = rule_db.search(db_piece).group(1)
		elif piece.has_key(dbname):
			piece[dbname].append(rule_db.search(db_piece).group(1))
		else:
			piece[dbname] = rule_db.findall(db_piece)
	result.append(piece)

#output test
for i in result:
	for j in i:
		if j == 'author' or j == 'translator':
			for k in i[j]:
				print k,
		else:
			print i[j],
	print

'''
#sql
conn = sqlite3.connect('books.db')
cur = conn.cursor()
cur.execute("create table if not exists books (doubanid,title,img,isbn10,isbn13,author1,author2,author3,translator1,translator2,translator3,price,publisher,pubdate)")
for i in result:
	cur.execute("select * from books where isbn10=?",i['isbn10'])
	first = cur.fetchone()
	if not first:
		cur.execute("insert into books values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",i)
#output
cur.execute('select * from timetable')
for i in range(0, 10):
	res = cur.fetchone()
	print 'row:', i+1
	for j in res:
		print j,
	print
print '-'*60
conn.commit()
cur.close()
conn.close()
'''
