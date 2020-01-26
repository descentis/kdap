from blm.kdap_wikiArticlesEditedMonthwiseCount import get_monthwise_articles_edited_count
from blm.kdap_wikiCategoryArticlesMonthwiseAuthors import get_monthly_authors_by_category
from blm.kdap_wikiCategoryArticlesMonthwiseRevisions import get_monthly_revision_count_by_category
from blm.kdap_wikiArticleRevisions import get_revisions_of_article
from blm.wiki_pageViews import get_pageviews
from blm.wikiExtract import wikiExtract
from matplotlib import pyplot as plt
import datetime
from dateutil.relativedelta import *
import time


# region usage graph
def create_x_and_y(data, template_name):
    raw_timestamps = list(data[template_name].keys())
    raw_timestamps.sort()
    timestamps = []
    y_articles = []
    for timestamp in raw_timestamps:
        year = int(timestamp[:4])
        month = int(timestamp[5:])
        if 2009 <= year < 2016:
            timestamps.append(year + month / 12)
            y_articles.append(data[template_name][timestamp])

    return timestamps, y_articles


def get_graph(template_name):
    plt.clf()
    articles_edited_count = get_monthwise_articles_edited_count(template_name)
    monthly_authors_count = get_monthly_authors_by_category(template_name)
    revisions_count = get_monthly_revision_count_by_category(template_name)
    for timestamp in monthly_authors_count[template_name]:
        monthly_authors_count[template_name][timestamp] = len(monthly_authors_count[template_name][timestamp])

    timestamps, y_articles = create_x_and_y(articles_edited_count, template_name)
    # plt.plot(timestamps, y_articles, label='Articles')

    timestamps, y_articles = create_x_and_y(monthly_authors_count, template_name)
    # plt.plot(timestamps, y_articles, label='Authors')

    timestamps, y_articles = create_x_and_y(revisions_count, template_name)
    # plt.plot(timestamps, y_articles, label='Revisions')

    # plt.yscale('log')
    # plt.legend(loc='best')
    # plt.show()

# endregion

# region jaccard graph
def get_x_coord(timestamp):
    year = int(timestamp[:4])
    month = int(timestamp[5:7])
    day = int(timestamp[8:10])

    x_coord = (year - 2014) * 365

    for i in range(1, month):
        if i in [1, 3, 5, 7, 8, 10, 12]:
            x_coord += 31
        elif i in [4, 6, 9, 11]:
            x_coord += 30
        else:
            x_coord += 28

    x_coord += day
    return x_coord


def get_jaccard_graph(template_name, focal_articles):
    # initialisation
    w = wikiExtract()
    template_articles_data = w.get_articles_by_template(template_name)[template_name]
    category_articles_data = w.get_articles_by_category(template_name)[template_name]
    category_articles_names = [data['title'] for data in category_articles_data]
    print(len(category_articles_names))
    template_articles_names = [data['title'] for data in template_articles_data]
    print(len(template_articles_names))
    category_articles = list(set(category_articles_names).union(set(template_articles_names)))
    print(len(category_articles))
    times_to_editors = {}  # mapping of timestamp to editors who edited then
    focal_times_to_editors = {}  # mapping of focal article name to {mapping of timestamp to editors}
    for article in focal_articles:
        focal_times_to_editors[article] = {}

    # getting and serialising data
    for article in category_articles:
        revisions = get_revisions_of_article(article)[article]
        for revision in revisions:
            if revision.get('user') is not None:
                timestamp = revision['timestamp'][:10]
                year = int(timestamp[:4])
                if year < 2016:  # !? or 2014 <= year < 2016
                    if timestamp not in times_to_editors:
                        times_to_editors[timestamp] = []
                    times_to_editors[timestamp].append(revision['user'])

                    if article in focal_articles:
                        if timestamp not in focal_times_to_editors[article]:
                            focal_times_to_editors[article][timestamp] = []
                        focal_times_to_editors[article][timestamp].append(revision['user'])

    # calculating graph coordinates
    sorted_times = sorted(times_to_editors.keys())
    points = {}
    cumulative_total = set()
    cumulative_focal = {}
    for article in focal_articles:
        cumulative_focal[article] = set()
        points[article] = []

    for timestamp in sorted_times:
        cumulative_total = cumulative_total.union(set(times_to_editors[timestamp]))
        for article in focal_articles:
            if timestamp in focal_times_to_editors[article]:
                cumulative_focal[article] = cumulative_focal[article].union(
                    set(focal_times_to_editors[article][timestamp]))
            year = int(timestamp[:4])
            if 2014 <= year < 2016:
                points[article].append((get_x_coord(timestamp), len(cumulative_focal[article]) / len(cumulative_total)))

    # for article in focal_articles:
    #     plt.plot([point[0] for point in points[article]], [point[1] for point in points[article]], label=article)

    xticks = [get_x_coord('2014-01-01'), get_x_coord('2014-04-01'), get_x_coord('2014-07-01'),
              get_x_coord('2014-10-01'), get_x_coord('2015-01-01'), get_x_coord('2015-04-01'),
              get_x_coord('2015-07-01'), get_x_coord('2015-10-01'), get_x_coord('2016-01-01')]
    xlabels = ['Jan 2014', 'Apr', 'Jul', 'Oct', 'Jan 2015', 'Apr', 'Jul', 'Oct', 'Jan 2016']

    # plt.xticks(xticks, xlabels)
    # plt.legend(loc='best')
    # plt.show()

# endregion


# region pageviews graph
def get_pageviews_graph(articles):
    pageviews = get_pageviews('wikipedia', article_name=articles, start='2015-07-01', end='2016-07-01',
                              granularity='daily')

    # for article in articles:
    #    plt.plot([(int(dt.strftime('%Y')) - 2015) * 365 + int(dt.strftime('%j')) for dt in pageviews.keys()],
    #             [pageviews[dt][article] for dt in pageviews.keys()], label=article.replace('_', ' '))

    xticks = []
    xlabels = []
    start_date = datetime.datetime(2015, 7, 1)
    end_date = datetime.datetime(2016, 7, 1)
    while start_date < end_date:
        xticks.append((int(start_date.strftime('%Y')) - 2015) * 365 + int(start_date.strftime('%j')))
        xlabels.append(start_date.strftime('%b-%Y'))
        start_date += relativedelta(months=1)

    # plt.xticks(xticks, xlabels, rotation=60)
    # plt.yscale('log')
    # plt.legend(loc='best')
    # plt.show()
# endregion


s = time.time()
get_pageviews_graph(['Ferguson_unrest', '2015_Baltimore_protests', 'Death_of_Freddie_Gray', 'Shooting_of_Michael_Brown'])

get_jaccard_graph('Black Lives Matter', ['Shooting of Michael Brown', 'Shooting of Trayvon Martin',
                                         'Shooting of Oscar Grant', 'Charleston Church Shooting', 'Ferguson unrest',
                                         'Black Lives Matter', 'Death of Eric Garner', 'Death of Freddie Gray',
                                         '2015 Baltimore protests', 'Death of Sandra Bland'])

get_graph('Black Lives Matter')
e = time.time()
print(e-s)