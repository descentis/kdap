import unittest
from kdap import analysis
import os
import shutil
import json


class TestAnalysis(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(__file__), 'testOutput/')
        self.ropar_filename = 'Indian_Institute_of_Technology_Ropar.knolml'
        self.zinc_filename = 'Zinc.knolml'
        self.k = analysis.knol()
        with open(os.path.dirname(__file__)+'/test_data.txt', 'r') as infile:
            self.frames_data = json.loads(infile.read())
        with open(os.path.dirname(__file__)+'/FL_Class.txt', 'r') as infile:
            self.class_data = infile.readlines()
        with open(os.path.dirname(__file__)+'/pageviews_data.json', 'r') as infile:
            self.views_data = json.loads(infile.read())[0]
        with open(os.path.dirname(__file__)+'/test_instance_dates.txt', 'r') as infile:
            self.instance_dates = infile.read().split(',')
        with open(os.path.dirname(__file__)+'/author_edits.txt', 'r') as infile:
            self.author_edits = json.load(infile)

    def get_wiki_article(self):
        article_name = 'IIT Ropar'
        self.k.get_wiki_article(article_name=article_name, output_dir=self.test_dir)
        self.assertTrue(os.path.exists(self.test_dir + self.ropar_filename))

    def test_download_dataset_article_list(self):
        self.k.download_dataset(sitename='wikipedia', article_list=['IIT Ropar', 'Zinc'], destdir=self.test_dir)
        self.assertTrue(os.path.exists(self.test_dir + self.ropar_filename))
        self.assertTrue(os.path.exists(self.test_dir + self.zinc_filename))
        self.frame_test()
        self.get_instance_date_test()

    def frame_test(self):
        test_data = {
            'id': [],
            'title': [],
            'bytes': [],
            'editor': [],
            'time': [],
            'text': [],
            'stats': []
        }
        for inst in self.k.frame(file_name=self.test_dir+self.ropar_filename):
            test_data['id'].append(inst.instanceId)
            test_data['title'].append(inst.get_title())
            test_data['bytes'].append(inst.get_bytes())
            test_data['editor'].append(inst.get_editor())
            test_data['time'].append(inst.get_timestamp())
            test_data['text'].append(inst.get_text())
            test_data['stats'].append(inst.get_text_stats())

        for key in self.frames_data.keys():
            self.assertTrue(all(x in self.frames_data[key] for x in test_data[key]))

    def test_get_pageviews(self):
        views = self.k.get_pageviews(site_name='wikipedia', article_name='Zinc', granularity='daily', start='20200828',
                                     end='20200917')
        for date in views:
            str_date = date.strftime('%Y-%m-%d')
            self.assertIn(str_date, self.views_data.keys())
            self.assertEqual(views[date]['Zinc'], self.views_data[str_date])

    def test_wiki_article_by_class(self):
        class_articles = self.k.get_wiki_article_by_class(wiki_class='FL')
        self.assertTrue(all(article in self.class_data for article in class_articles))

    def get_instance_date_test(self):
        dates = self.k.get_instance_date(file_list=self.test_dir+self.ropar_filename).values()[0]
        self.assertLessEqual(len(dates), len(self.instance_dates))
        self.assertTrue(all(date in self.instance_dates for date in dates))

    def author_edits_test(self):
        edits = self.k.get_author_edits(article_list=self.test_dir+self.ropar_filename, editor_list='Awadh2020')
        for key in edits.keys():
            edits[key] = edits[key][self.test_dir+self.ropar_filename]
            self.assertIn(key, self.author_edits.keys())
            self.assertEqual(edits[key], self.author_edits[key])

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists('outputD/'):
            shutil.rmtree('outputD/')
