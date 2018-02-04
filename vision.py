import cv2
from mss import mss
from PIL import Image
import numpy as np
import time

class Vision:
    def __init__(self):
        self.static_templates = {
            'left-goalpost': '/home/flakas/code/burrito_bison/assets/left-goalpost.png',
            'bison-head': '/home/flakas/code/burrito_bison/assets/bison-head.png',
            'pineapple-head': '/home/flakas/code/burrito_bison/assets/pineapple-head.png',
            'bison-health-bar': '/home/flakas/code/burrito_bison/assets/bison-health-bar.png',
            'pineapple-health-bar': '/home/flakas/code/burrito_bison/assets/pineapple-health-bar.png',
            'cancel-button': '/home/flakas/code/burrito_bison/assets/cancel-button.png',
            'filled-with-goodies': '/home/flakas/code/burrito_bison/assets/filled-with-goodies.png',
            'next-button': '/home/flakas/code/burrito_bison/assets/next-button.png',
            'tap-to-continue': '/home/flakas/code/burrito_bison/assets/tap-to-continue.png',
            'unlocked': '/home/flakas/code/burrito_bison/assets/unlocked.png',
            'full-rocket': '/home/flakas/code/burrito_bison/assets/full-rocket.png'
        }

        self.templates = { k: cv2.imread(v, 0) for (k, v) in self.static_templates.items() }

        self.monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
        self.screen = mss()

        self.frame = None

    def take_screenshot(self):
        sct_img = self.screen.grab(self.monitor)
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        img = np.array(img)
        img = self.convert_rgb_to_bgr(img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        return img_gray

    def get_image(self, path):
        return cv2.imread(path, 0)

    def bgr_to_rgb(self, img):
        b,g,r = cv2.split(img)
        return cv2.merge([r,g,b])

    def convert_rgb_to_bgr(self, img):
        return img[:, :, ::-1]

    def match_template(self, img_grayscale, template, threshold=0.9):
        """
        Matches template image in a target grayscaled image
        """

        res = cv2.matchTemplate(img_grayscale, template, cv2.TM_CCOEFF_NORMED)
        matches = np.where(res >= threshold)
        return matches

    def find_template(self, name, image=None, threshold=0.9):
        if image is None:
            if self.frame is None:
                self.refresh_frame()

            image = self.frame

        return self.match_template(
            image,
            self.templates[name],
            threshold
        )

    def scaled_find_template(self, name, image=None, threshold=0.9, scales=[1.0, 0.9, 1.1]):
        if image is None:
            if self.frame is None:
                self.refresh_frame()

            image = self.frame

        initial_template = self.templates[name]
        for scale in scales:
            scaled_template = cv2.resize(initial_template, (0,0), fx=scale, fy=scale)
            matches = self.match_template(
                image,
                scaled_template,
                threshold
            )
            if np.shape(matches)[1] >= 1:
                return matches
        return matches

    def refresh_frame(self):
        self.frame = self.take_screenshot()
