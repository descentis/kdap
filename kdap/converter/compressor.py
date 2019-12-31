import difflib
import xml.etree.ElementTree as ET
import math
import os

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def encode(str1, str2):
	output = ""
	s = [x.replace("\n", "`").replace("-", "^") for x in str1.split(" ")]

	s2 = [x.replace("\n", "`").replace("-", "^") for x in str2.split(" ")]

	i = 0
	while(True):
		if i == len(s):
			break;
		if s[i].isspace() or s[i] == '':
			del s[i]
		else:	
			i += 1	
	i = 0
	while(True):
		if i == len(s2):
			break;
		if s2[i].isspace() or s2[i] == '':
			del s2[i]
		else:	
			i += 1	
			
	d = difflib.Differ()

	result = list(d.compare(s, s2))

	pos = 0
	neg = 0

	for x in result:
		if x[0] == " ":
			pos += 1
			if neg != 0:
				output += "-"+str(neg)+" "
				neg = 0
		elif x[0] == "-":
			neg += 1
			if pos != 0:
				output += str(pos)+" "
				pos = 0	
		elif x[0] != "?":
			if pos != 0:
				output += str(pos)+" "
				pos = 0	
			if neg != 0:
				output += "-"+str(neg)+" "
				neg = 0
			if is_number(x[2:]):
				output += "'"+x[2:]+"' "
			else:			
				output += x[2:]+" "
	if pos != 0:
		output += str(pos)+" "
	if neg != 0:
		output += "-"+str(neg)+" "
	return output.replace("\t\t\t", "")

#Main function

def compress(file_name, directory):
	# file_name = input("Enter path of KML file:")

    tree = ET.parse(file_name)
    r = tree.getroot()
    for child in r:
        if('KnowledgeData' in child.tag):
            root = child
            
    last_rev = ""
    length = len(root.findall('Instance'))

    print(length, "revisions found")

    count = 0
    intervalLength =  int((math.log(length)) ** 2);  

    # Keep the Orginal text after every 'm' revisions
    m = intervalLength+1
    for each in root.iter('Text'):
        count += 1
        if m != intervalLength+1:
            current_str = each.text
            each.text = encode(prev_str, current_str)
            prev_str = current_str
            # print("Revision ", count, " written")
			
            m = m - 1
            if m == 0:
                m = intervalLength+1
        else:
            prev_str = each.text
            # print("Revision ", count, " written")
            m = m - 1
            continue

    print("KNML file created")
	
    # Creating directory 
    if not os.path.exists(directory):
        os.mkdir(directory)

    # Changing file path to include directory
    file_name = file_name.split('/')
    file_name = directory+'/'+file_name[-1]
    '''
    file_name.insert(-1, directory)
    separator = '/'
    file_name = separator.join(file_name)
    '''

    tree.write(file_name[:-7]+'Compressed.knolml')
    f = open(file_name[:-7]+'Compressed.knolml')
    f_str = f.read()
    f.close()

    f2 = open(file_name[:-7]+'Compressed.knolml', "w")
    f2.write("<?xml version='1.0' encoding='utf-8'?>\n"+f_str)
    f2.close()
