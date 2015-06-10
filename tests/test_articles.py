#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_articles
----------------------------------

Tests for `articles` module.
"""

import unittest

from articles import articles


class TestArticles(unittest.TestCase):

    def setUp(self):
        self.doi = articles.test_dois[0]
        self.assertGreater(len(self.doi), 0)

    def test_articles(self):
        self.doc = articles.DOI(self.doi)

    def tearDown(self):
        self.doc.graph.close()

if __name__ == '__main__':
    unittest.main()
