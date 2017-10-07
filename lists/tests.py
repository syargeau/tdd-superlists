from django.test import TestCase

class SmokeTest(TestCase):
    """
    Simple test to make sure our unit tests are being incorporated.
    """

    def test_bad_math(self):
        """
        Test that inequality is recognized and works.
        """
        self.assertEqual(1 + 1, 3)
