import xml.etree.ElementTree as ET


def get_aa_questions():
    posts_tree = ET.parse("anime.stackexchange.com/Posts.xml")
    posts_root = posts_tree.getroot()
    aa_questions = []
    for post in posts_root:
        if post.get('PostTypeId') == '1' and 'AcceptedAnswerId' in post.attrib:
            aa_questions.append(post)

    '''
    format:
    <root>
        <question Id='' AcceptedAnswerId='' Title=''>
        ...Body...
        </question>
    </root>
    '''
    aaques_root = ET.Element('root')
    for i in range(len(aa_questions)):
        ET.SubElement(aaques_root, 'question', {'Id': aa_questions[i].get('Id'),
                                   'AcceptedAnswerId': aa_questions[i].get('AcceptedAnswerId'),
                                   'Title': aa_questions[i].get('Title')})
        aaques_root[i].text = aa_questions[i].get('Body')
    aaques_tree = ET.ElementTree(aaques_root)
    aaques_tree.write('stackex_accepted_answer_questions.xml')


'''
import time
s = time.time()
get_aa_questions()
e = time.time()
print(e-s)
'''