from crowd_diversity import data_serialise, control_variables, independent_variables, mediators
import json
import time

s = time.time()
print('s')
data_serialise.get_all_articles_data(['Geography', 'History', 'Philosophy', 'Religion', 'Mathematics', 'Sociology',
                                      'Technology', 'Science', 'Culture'])

with open("articles_data.json", "r") as fh:
    all_articles = json.load(fh)['all_articles']

for article in all_articles:
    print(control_variables.article_age(article),
          control_variables.article_size(article),
          control_variables.average_experience(article),
          mediators.task_communication(article),
          mediators.task_conflict(article),
          independent_variables.contribution_diversity(article),
          independent_variables.experience_diversity(article))
e = time.time()
print('e')
print(e - s)
