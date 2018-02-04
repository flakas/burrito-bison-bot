import cv2
import numpy as np

from vision import Vision
from controller import Controller
from game import Game

vision = Vision()
controller = Controller()
game = Game(vision, controller)

# screenshot = vision.get_image('tests/screens/round-finished-results.png')
# print(screenshot)
# match = vision.find_template('bison-head', image=screenshot)
# print(np.shape(match)[1])

game.run()
