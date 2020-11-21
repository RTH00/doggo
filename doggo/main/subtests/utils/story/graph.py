from django.test import TestCase

from main.utils.story.graph import graph_sanity_check


class UtilsStoryGraphTests(TestCase):

    def test_graph_valid(self):
        """
        Check the Graph is valid
        :return:
        """
        self.assertTrue(graph_sanity_check())
