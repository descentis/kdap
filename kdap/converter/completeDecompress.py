import xml.etree.ElementTree as ET
import xml.dom.minidom
import math

file_name = input("Enter compressed KNML file path: ")

tree = ET.parse(file_name)
root = tree.getroot()
last_rev = ""
count = 0
length = len(root[0].findall('Instance'))

if length == 1:
	print("No revisions found, generate revisions from xmltoknml.py first")
	exit()

revisionsDict = {}

for each in root.iter('Instance'):
	instanceId = int(each.attrib['Id'])
	for child in each:
		if 'Body' in child.tag:
			revisionsDict[instanceId] = child[0].text


# n = int(input(str(length)+" Revisons found, enter the revision number to be loaded: "))
# original = n

for n in range(1, length+1):
	original = n
	m = int((math.log(length)) ** 2)+1;
	if n%m != 0:
		interval = n - (n%m) + 1
		n = n - interval + 1
	else:
		interval = n - (m-1)
		n = n - interval + 1


	count = interval
	prev_str = revisionsDict[count]
	result = prev_str
	while count < original:
		count += 1
		s = [x.replace("\n", "`").replace("-", "^") for x in prev_str.split(" ")]
		i = 0
		while(True):
			if i == len(s):
				break;
			if s[i].isspace() or s[i] == '':
				del s[i]
			else:	
				i += 1	

		next_rev = revisionsDict[count]
		s2 = next_rev.split(" ")
		i = 0
		while(True):
			if i == len(s2):
				break;
			if s2[i].isspace() or s2[i] == '':
				del s2[i]
			else:	
				i += 1	

		index = 0
		result = ""
		for x in s2:
			if x.isdigit():
				for i in range(index, index+int(x)):
		#			print(s[i], end=" ")
					result += s[i].replace("`", "\n").replace("^", "-")
					result += " "
					index += 1
			elif x[0] == "'" and x[-1] == "'" and x[1:-1].isdigit():
		#			print(x[1:-1].replace("`", "\n").replace("~", "-"), end=" ")				 
					result += x[1:-1].replace("`", "\n			").replace("^", "-")
					result += " "
			else:
				if x[0] == '-':
					for i in range(index, index+int(x[1:])):
						index += 1
				else:
		#			print(x.replace("`", "\n").replace("~", "-"), end=" ")
					result += x.replace("`", "\n			").replace("^", "-")		
					result += " "

		prev_str = result

	for each in root[0].findall('Instance')[original-1]:
		if 'Body' in each.tag:
			each[0].text = result

tree.write('output.knml')
print("All", original, "revisions written to output.knml")

f = open('output.knml')
f_str = f.read()
f.close()

f2 = open('output.knml', "w")
f2.write("<?xml version='1.0' encoding='utf-8'?>\n"+f_str)
f2.close()