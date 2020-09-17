import unittest
from kdap import analysis
import os
import shutil


class TestAnalysis(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'testOutput/'
        self.ropar_filename = 'Indian_Institute_of_Technology_Ropar.knolml'
        self.zinc_filename = 'Zinc.knolml'
        self.k = analysis.knol()

    def get_wiki_article(self):
        article_name = 'IIT Ropar'
        self.k.get_wiki_article(article_name=article_name, output_dir=self.test_dir)
        self.assertTrue(os.path.exists(self.test_dir + self.ropar_filename))
        os.remove(self.test_dir + self.ropar_filename)

    def test_download_dataset_article_list(self):
        site = 'wikipedia'
        self.k.download_dataset(sitename=site, article_list=['IIT Ropar', 'Zinc'], destdir=self.test_dir)
        self.assertTrue(os.path.exists(self.test_dir + self.ropar_filename))
        self.assertTrue(os.path.exists(self.test_dir + self.zinc_filename))

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists('outputD/'):
            shutil.rmtree('outputD/')
