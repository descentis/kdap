from blm.wiki_pageViews import get_pageviews
from matplotlib import pyplot as plt
import datetime
from dateutil.relativedelta import *


def get_pageviews_graph(articles):
    pageviews = get_pageviews('wikipedia', article_name=articles, start='2015-07-01', end='2016-07-01',
                              granularity='daily')

    for article in articles:
        plt.plot([(int(dt.strftime('%Y')) - 2015) * 365 + int(dt.strftime('%j')) for dt in pageviews.keys()],
                 [pageviews[dt][article] for dt in pageviews.keys()], label=article.replace('_', ' '))

    xticks = []
    xlabels = []
    start_date = datetime.datetime(2015, 7, 1)
    end_date = datetime.datetime(2016, 7, 1)
    while start_date < end_date:
        xticks.append((int(start_date.strftime('%Y')) - 2015) * 365 + int(start_date.strftime('%j')))
        xlabels.append(start_date.strftime('%b-%Y'))
        start_date += relativedelta(months=1)

    plt.xticks(xticks, xlabels, rotation=60)
    plt.yscale('log')
    plt.legend(loc='best')
    plt.show()


get_pageviews_graph(['Ferguson_unrest', '2015_Baltimore_protests', 'Death_of_Freddie_Gray', 'Shooting_of_Michael_Brown'])
