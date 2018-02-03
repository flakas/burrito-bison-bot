from unittest import TestCase
from unittest.mock import Mock
from vision import Vision
import numpy as np

class VisionTest(TestCase):

    def setUp(self):
        self.vision = Vision()

    def test_finds_finished_mission(self):
        screenshot = self.vision.get_image('tests/screens/round-finished-missions.png')
        match = self.vision.find_template('tap-to-continue', screenshot)
        self.assertEqual(np.shape(match)[1], 1)

    def test_finds_next_button(self):
        screenshot = self.vision.get_image('tests/screens/round-finished-results.png')
        match = self.vision.find_template('next-button', screenshot)
        self.assertEqual(np.shape(match)[1], 1)

    def test_finds_round_starting_indicator(self):
        screenshot = self.vision.get_image('tests/screens/round-started.png')
        match = self.vision.find_template('health-bar', screenshot)
        self.assertEqual(np.shape(match)[1], 1)

    def test_finds_bison_head(self):
        screenshot = self.vision.get_image('tests/screens/round-started.png')
        match = self.vision.find_template('bison-head', screenshot)
        self.assertEqual(np.shape(match)[1], 1)
