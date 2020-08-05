import xml.etree.ElementTree as ET
import random


def random_questions(count):
    posts_tree = ET.parse('anime.stackexchange.com/Posts.xml')
    question_tags = []
    answer_tags = []
    posts_root = posts_tree.getroot()
    for row in posts_root:
        if row.get('PostTypeId') == "1":
            question_tags.append(row)
        elif row.get('PostTypeId') == "2":
            answer_tags.append(row)

    comment_parent_ids = []
    question_tags = random.choices(question_tags, k=count)
    question_ids = [q.get('Id') for q in question_tags]
    chosen_answers = {q_id: [] for q_id in question_ids}
    for answer in answer_tags:
        if answer.get('ParentId') in question_ids:
            chosen_answers[answer.get('ParentId')].append(answer)
            comment_parent_ids.append(answer.get('Id'))

    comment_parent_ids.extend(question_ids)

    '''
    format:
    <root>
        <question Id='' Body='' Title=''>
            <answer Id=''>
            ...answer...
            </answer>
        </question>
    </root>
    '''
    qa_root = ET.Element("root")
    for i in range(len(question_ids)):
        ET.SubElement(qa_root, 'question', {'Id': question_ids[i],
                                            'Title': question_tags[i].get('Title'),
                                            'Body': question_tags[i].get('Body')})
        for j in range(len(chosen_answers[question_ids[i]])):
            ET.SubElement(qa_root[i], 'answer', {'Id': chosen_answers[question_ids[i]][j].get('Id')})
            qa_root[i][j].text = chosen_answers[question_ids[i]][j].get('Body')

    qa_tree = ET.ElementTree(qa_root)
    qa_tree.write("stackex_qa_data.xml")

    '''
    format:
    <root>
        <comment Id='' ParentId=''>
            ...
        </comment>
    </root>
    '''

    comments_tree = ET.parse('anime.stackexchange.com/Comments.xml')
    comments_root = comments_tree.getroot()

    related_comments = []
    for row in comments_root:
        if row.get('PostId') in comment_parent_ids:
            related_comments.append(row)

    relcomm_root = ET.Element('root')
    for i in range(len(related_comments)):
        ET.SubElement(relcomm_root, 'comment', {'Id': related_comments[i].get('Id'),
                                                'ParentId': related_comments[i].get('PostId')})
        relcomm_root[i].text = related_comments[i].get('Text')

    relcomm_tree = ET.ElementTree(relcomm_root)
    relcomm_tree.write('stackex_comment_data.xml')


'''
tree = ET.parse('stackex_qa_data.xml')
root = tree.getroot()
c = 0
for child in root.iter('question'):
    c += 1
print(c)
'''
