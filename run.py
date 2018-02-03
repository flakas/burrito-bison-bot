import cv2
import numpy as np
from matplotlib import pyplot as plt
import random
from pynput.mouse import Button, Controller
import time
from mss import mss
from PIL import Image
from vision import Vision

vision = Vision()

screenshot = vision.get_image('tests/screens/round-finished-results.png')
print(screenshot)
match = vision.find_template('bison-head', image=screenshot)
print(np.shape(match)[1])
