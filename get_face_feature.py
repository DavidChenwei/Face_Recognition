from ctypes import string_at
from io import BytesIO

import cv2
import numpy as np

from face_recognition import implement_method


def extract_features(buffer_data):
    """
    :param buffer_data: 图片的二进制
    :return 图片的特征
    """
    #  将二进制转换成图像
    img_np_arr = np.frombuffer(buffer_data, np.uint8)
    image = cv2.imdecode(img_np_arr, cv2.IMREAD_COLOR)
    cv2.imshow('test', image)
    cv2.waitKey()
    #  调用face_detect方法得出每张图片的脸部特征
    res = im.face_detect(image)
    # print(face_feature)
    return res


if __name__ == '__main__':
    # 实例化对象
    im = implement_method()

    # 读取数据库中用户ID和图片二进制数据
    user_dict = im.read_pic()

    # 获取脸部特征并更新用户字典为UserID:features
    for key, value in user_dict.items():
        print(value)
        face_feature = extract_features(value)
        f = BytesIO(string_at(face_feature.feature, face_feature.featureSize))
        # 将图片特征的二进制表示存入字典中
        user_dict[key] = f.getvalue()

    # 将更新后的user_dict存入数据库中的FaceInfo列
    im.update_date(user_dict)
