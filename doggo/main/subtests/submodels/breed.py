from django.test import TestCase

from main.submodels.breed import BREED_PROPERTIES, BreedType, build_decreasing_rate, build_proba


class SubmodelsBreedTests(TestCase):

    def test_all_breeds_have_properties(self):
        for attr, value in BreedType.__dict__.items():
            if '__' not in attr:
                self.assertIsNotNone(BREED_PROPERTIES[value])

    def test_build_decreasing_rate(self):
        self.assertEqual(0.0002777777777777778, build_decreasing_rate(1))
        self.assertEqual(0.0001388888888888889, build_decreasing_rate(2))
        self.assertEqual(2.777777777777778e-05, build_decreasing_rate(10))

    def test_build_proba(self):
        self.assertEqual(0.1, build_proba(10))
        self.assertEqual(1.0, build_proba(1))
