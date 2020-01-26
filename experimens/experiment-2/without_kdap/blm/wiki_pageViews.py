from mwviews.api import PageviewsClient


def get_pageviews(site_name, *args, **kwargs):
    if site_name.lower() == 'wikipedia':
        start = ''
        end = ''
        granularity = 'monthly'
        if kwargs.get('article_name') != None:
            article_name = kwargs['article_name']
        # article_name = self.get_article_name(article_name)
        if kwargs.get('start') != None:
            start = kwargs['start'].replace('-', '')

        if kwargs.get('end') != None:
            end = kwargs['end'].replace('-', '')

        if kwargs.get('granularity') != None:
            granularity = kwargs['granularity']

        p = PageviewsClient(user_agent="<person@organization.org>")

        if start == '':
            return p.article_views('en.wikipedia', article_name, granularity=granularity)
        elif end == '':
            return p.article_views('en.wikipedia', article_name, granularity=granularity, start=start, end=start)
        else:
            return p.article_views('en.wikipedia', article_name, granularity=granularity, start=start, end=end)
