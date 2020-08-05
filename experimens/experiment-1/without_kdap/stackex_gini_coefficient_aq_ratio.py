import statistics
import xml.etree.ElementTree as ET
import scipy.stats as ss


def get_gini_coefficient(portal_dir):
    posts_root = ET.parse(portal_dir + '/Posts.xml').getroot()
    user_contribs = {}
    for post in posts_root:
        u_id = post.get('OwnerUserId')
        if u_id not in user_contribs:
            user_contribs[u_id] = 0
        user_contribs[u_id] += len(post.get('Body').encode('utf-8'))

        if post.get('PostTypeId') == '1':
            user_contribs[u_id] += len(post.get('Title').encode('utf-8'))

    comments_root = ET.parse(portal_dir + '/Comments.xml').getroot()
    for comment in comments_root:
        u_id = comment.get('UserId')
        if u_id not in user_contribs:
            user_contribs[u_id] = 0
        user_contribs[u_id] += len(comment.get('Text').encode('utf-8'))

    absolute_difference_sum = 0
    for val1 in user_contribs.values():
        for val2 in user_contribs.values():
            absolute_difference_sum += abs(val1 - val2)

    mean = statistics.mean(list(user_contribs.values()))
    gini = absolute_difference_sum / (2 * len(user_contribs) ** 2 * mean)
    return gini


def get_answer_to_question_ratio(portal_dir):
    posts_tree = ET.parse(portal_dir + '/Posts.xml')
    posts_root = posts_tree.getroot()
    question_count = 0
    answer_count = 0
    for post in posts_root:
        if post.get('PostTypeId') == '1':
            question_count += 1
        else:
            answer_count += 1

    return answer_count/question_count


def get_correlation(portal_dirs):
    gini_coefficients = []
    a_to_q_ratios = []
    for portal_dir in portal_dirs:
        gini_coefficients.append(get_gini_coefficient(portal_dir))
        a_to_q_ratios.append(get_answer_to_question_ratio(portal_dir))
    return ss.pearsonr(gini_coefficients, a_to_q_ratios)


'''
import time
s = time.time()
get_correlation(['3dprinting.stackexchange.com', 'ai.stackexchange.com', 'anime.stackexchange.com',
                       'arduino.stackexchange.com', 'boardgames.stackexchange.com', 'chemistry.stackexchange.com',
                       'chess.stackexchange.com'])
e = time.time()
print(e-s)
'''
'''
print(get_gini_coefficient('anime.stackexchange.com'))
print(get_answer_to_question_ratio('anime.stackexchange.com'))
'''