import re

import cv2
import numpy as np
import requests
from aip import AipOcr

from cred_loader import APP_ID, API_KEY, SECRET_KEY

MAX_RETRY = 5

ocr_client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def _convert(src):
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    low_hsv = np.array([0, 0, 0])
    high_hsv = np.array([180, 255, 46])
    mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)
    mask = 255 - mask  # invert color
    mask = mask[10:28, 20:130]  # crop

    # Reduce noise
    for i in range(1, mask.shape[0] - 1):
        for j in range(1, mask.shape[1] - 1):
            if mask[i, j] == 0 \
                    and mask[i - 1, j] == 255 and mask[i + 1, j] == 255 \
                    and mask[i, j - 1] == 255 and mask[i, j + 1] == 255:
                mask[i, j] = 255

    # cv2.imwrite('file.png', mask)  # debug

    success, encoded_image = cv2.imencode('.png', mask)
    return encoded_image.tobytes()


def recognize(captcha_url: str):
    r = requests.get(captcha_url)
    image = np.asarray(bytearray(r.content))
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    png_cv_bytes = _convert(image)

    result_json = ocr_client.basicGeneral(png_cv_bytes)
    if 'error_code' in result_json:
        # failed
        result_code = ''
    else:
        result_code = result_json['words_result'][0]['words']
        result_code = re.sub(r'[\W_]+', '', result_code)  # 只保留字母和数字
        result_code = result_code.upper()  # 只有大写字母

    return result_code
