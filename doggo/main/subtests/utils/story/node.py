from typing import Callable, Dict

from django.test import TestCase

from main.submodels.dog import Dog
from main.utils.story.node import Node, Choice, sample_node_links, NodeLink, find_choice


DOG_TO_STR: Callable[[Dog], str] = lambda dog: "something"


class UtilsStoryNodeTests(TestCase):

    def test_choices_sanity_check_1(self):
        """
        Test with choices = empty list
        :return:
        """
        self.assertTrue(
            Node(
                id="1",
                text=DOG_TO_STR,
                choices=[],
                effect=lambda account, dog: None
            ).choices_sanity_check()
        )

    def test_choices_sanity_check_2(self):
        """
        Test with one choice
        :return:
        """
        self.assertTrue(
            Node(
                id="1",
                text=DOG_TO_STR,
                choices=[Choice("1", DOG_TO_STR, [NodeLink("1", 1)])],
                effect=lambda account, dog: None
            ).choices_sanity_check()
        )

    def test_choices_sanity_check_3(self):
        """
        Test with choices = two different choice ids
        :return:
        """
        self.assertTrue(
            Node(
                id="1",
                text=DOG_TO_STR,
                choices=[Choice("1", DOG_TO_STR, [NodeLink("1", 1)]), Choice("2", DOG_TO_STR, [NodeLink("1", 1)])],
                effect=lambda account, dog: None
            ).choices_sanity_check()
        )

    def test_choices_sanity_check_4(self):
        """
        Test with choices = two same choice ids
        :return:
        """
        with self.assertRaises(Exception):
            Node(
                id="1",
                text=DOG_TO_STR,
                choices=[Choice("1", DOG_TO_STR, [NodeLink("1", 1)]), Choice("1", DOG_TO_STR, [NodeLink("1", 1)])],
                effect=lambda account, dog: None
            ).choices_sanity_check()

    def test_choices_sanity_check_5(self):
        """
        Test with a choice without link
        :return:
        """
        with self.assertRaises(Exception):
            Node(
                id="1",
                text=DOG_TO_STR,
                choices=[Choice("1", DOG_TO_STR, [])],
                effect=lambda account, dog: None
            ).choices_sanity_check()

    def test_sample_node_links_1(self):
        with self.assertRaises(Exception):
            sample_node_links([])

    def test_sample_node_links_2(self):
        self.assertEqual("1", sample_node_links([NodeLink("1", 1)]))

    def test_sample_node_links_3(self):
        """
        Test the distribution
        :return:
        """
        counters: Dict[str, int] = {}
        node_links: [NodeLink] = [
            NodeLink("1", 1),
            NodeLink("2", 1),
            NodeLink("3", 3),
            NodeLink("4", 1)
        ]
        for node in node_links:
            counters[node.node_id] = 0
        for i in range(10000):
            node_id: str = sample_node_links(node_links)
            counters[node_id] += 1
        self.assertGreater(counters["1"], 1500)
        self.assertLess(counters["1"], 1800)
        self.assertGreater(counters["2"], 1500)
        self.assertLess(counters["2"], 1800)
        self.assertGreater(counters["3"], 4500)
        self.assertLess(counters["3"], 5500)
        self.assertGreater(counters["4"], 1500)
        self.assertLess(counters["4"], 1800)

    def test_sample_node_links_4(self):
        """
        Test the distribution
        :return:
        """
        counters: Dict[str, int] = {}
        node_links: [NodeLink] = [
            NodeLink("1", 9),
            NodeLink("2", 1)
        ]
        for node in node_links:
            counters[node.node_id] = 0
        for i in range(10000):
            node_id: str = sample_node_links(node_links)
            counters[node_id] += 1
        self.assertGreater(counters["1"], 8500)
        self.assertLess(counters["1"], 9500)
        self.assertGreater(counters["2"], 500)
        self.assertLess(counters["2"], 1500)

    def test_sample_node_links_5(self):
        """
        Test the distribution
        :return:
        """
        counters: Dict[str, int] = {}
        node_links: [NodeLink] = [
            NodeLink("1", 1),
            NodeLink("2", 9)
        ]
        for node in node_links:
            counters[node.node_id] = 0
        for i in range(10000):
            node_id: str = sample_node_links(node_links)
            counters[node_id] += 1
        self.assertGreater(counters["1"], 500)
        self.assertLess(counters["1"], 1500)
        self.assertGreater(counters["2"], 8500)
        self.assertLess(counters["2"], 9500)

    def test_find_choice_1(self):
        self.assertIsNone(find_choice('', []))

    def test_find_choice_2(self):
        choice: Choice = Choice("2", DOG_TO_STR, [])
        self.assertEqual(choice, find_choice('2', [
            Choice("1", DOG_TO_STR, []),
            choice,
            Choice("3", DOG_TO_STR, []),
        ]))

    def test_find_choice_3(self):
        self.assertIsNone(find_choice('4', [
            Choice("1", DOG_TO_STR, []),
            Choice("2", DOG_TO_STR, []),
            Choice("3", DOG_TO_STR, []),
        ]))
