from time import sleep

import cv2
import numpy as np
import pyautogui
import pyocr
import pyocr.builders
from PIL import Image, ImageGrab

TRIM_POS = (1474, 369, 2434, 1809)


def trim_img(file_name):
    img = Image.open(file_name)
    img_trim = img.crop(TRIM_POS)
    img_trim.save('trim.png')
    return img_trim


def capture():
    img = ImageGrab.grab(bbox=TRIM_POS)
#     img = img.resize((img.width // 2, img.height // 2))
    img.save("capture.png")
    return img


def bin_img(file_name):
    img = cv2.imread(file_name)
    black_min = np.array([100, 100, 150], np.uint8)
    black_max = np.array([255, 255, 255], np.uint8)
    img_bin = cv2.inRange(img, black_min, black_max)
    cv2.imwrite('./bin.png', img_bin)
    return img_bin


def find_txt(file_name):
    tool = pyocr.get_available_tools()[0]
    lang = tool.get_available_languages()[0]
    text = tool.image_to_string(Image.open(file_name), lang=lang, builder=pyocr.builders.TextBuilder(tesseract_layout=6))
    texts = [x for x in text.split('\n')]
    texts = [''.join([c.lower() for c in text if c.isalpha()]) for text in texts]
    texts = [x for x in texts if x]
    print(texts)
    return texts


def input_key(texts):
    for text in texts:
        pyautogui.typewrite(text, interval=0)
        pyautogui.typewrite(['backspace'])


def main():
    while True:
        capture()
        bin_img('capture.png')
        texts = find_txt('bin.png')
        input_key(texts)
        sleep(0.5)


if __name__ == "__main__":
    main()
