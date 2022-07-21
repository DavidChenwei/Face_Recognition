from ctypes import string_at
from io import BytesIO

import cv2
import numpy as np

from face_recognition import implement_method


def extract_features(buffer_data):
    """
    :param buffer_data: image binary
    :return: Features of the picture
    """
    #  Convert binary to image
    img_np_arr = np.frombuffer(buffer_data, np.uint8)
    image = cv2.imdecode(img_np_arr, cv2.IMREAD_COLOR)
    cv2.imshow('test', image)
    cv2.waitKey()
    #  Call the face_detect method to get the facial features of each image
    res = im.face_detect(image)
    # print(face_feature)
    return res


if __name__ == '__main__':
    im = implement_method()

    # Read binary data of user ID and picture from database
    user_dict = im.read_pic()

    # Get facial features and update the user dictionary to UserID:features
    for key, value in user_dict.items():
        print(value)
        face_feature = extract_features(value)
        f = BytesIO(string_at(face_feature.feature, face_feature.featureSize))
        # Store the binary representation of the image features in a dictionary
        user_dict[key] = f.getvalue()

    # Store the updated user_dict in the FaceInfo column in the database
    im.update_date(user_dict)
