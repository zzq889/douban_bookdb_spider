#_*_encoding:utf-8_*_
#!/usr/bin/env python
import re

content = open('tags.html','r').read()
result1 = re.findall(r'<tbody.+?</tbody', content, re.S)
rule = re.compile(r'">(.+?)</a><b>', re.S)
result = []
for i in result1:
	result.append(rule.findall(i))

file = open('taglist','wb')
for i in result:
	for j in i:
		file.write(j)
		file.write('\n')
file.close()
