import traceback

import cv2
import numpy as np
import pymysql

from arcface.engine import *


class implement_method():
    """
    类:以及其包含的方法
    """

    def __init__(self):
        # 初始化用户字典
        self.user_dict = {}

        # 初始化特征字典
        self.feature_dict = {}

        # 设置APP ID和SDK KEY
        appid = b'Smxn3HaVJQN4R9TvAb5cpdd1atGLfoZHULG82XBMqhV'
        sdk_key = b'BpHQEL4momrZJK6NYKEnfxHPYsd7NN83NvzcvGQ7iLn3'

        if os.path.exists('ArcFace64.dat'):
            # 获取人脸识别引擎
            self.face_engine = ArcFace()
            print('已获认证，开启人脸识别引擎')
        else:
            # 激活接口,首次需联网激活
            res = ASFOnlineActivation(appid, sdk_key)
            if MOK != res and MERR_ASF_ALREADY_ACTIVATED != res:
                print("ASFActivation fail: {}".format(res))
            else:
                print("ASFActivation sucess: {}".format(res))

            # 获取激活文件信息
            res, active_file_info = ASFGetActiveFileInfo()

            if (res != MOK):
                print("ASFGetActiveFileInfo fail: {}".format(res))
            else:
                print(active_file_info)
            # 获取人脸识别引擎
            self.face_engine = ArcFace()
            print('通过认证，已开启人脸识别引擎')

        # 需要引擎开启的功能
        self.mask = ASF_FACE_DETECT | ASF_FACERECOGNITION | ASF_AGE | ASF_GENDER | ASF_FACE3DANGLE | ASF_LIVENESS | ASF_IR_LIVENESS

        # 初始化接口
        res = self.face_engine.ASFInitEngine(ASF_DETECT_MODE_IMAGE, ASF_OP_0_ONLY, 30, 10, self.mask)
        if res != MOK:
            print("ASFInitEngine fail: {}".format(res))
        else:
            print("ASFInitEngine sucess: {}".format(res))

        #  初始化数据库链接
        self.conn = pymysql.connect(host='192.168.2.8', user='admin', password='admin123', database='zua_virtualcenter',
                                    charset='utf8')

    # 检查数据库是否连接
    def is_connect(self):
        """
        检查数据库是否连接，若没有则连接
        """
        try:
            self.conn.ping(reconnect=True)
            print("db is connecting")
        except Exception as e:
            traceback.print_exc()
            self.conn = self.to_connect()
            print("db reconnect")

    # 读取数据库中用户图像的方法
    def read_pic(self):
        """
        :return: 用户字典。UserID : 图片二进制数据
        """
        cursor = self.conn.cursor()
        sql = 'SELECT UserID,FaceInfo FROM base_user'
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for item in results:
                user_id = item[0]
                face_info = item[1]
                if face_info is not None:
                    self.user_dict[user_id] = face_info
        except Exception as e:
            print("Error: " + e)
        cursor.close()
        self.conn.close()

        return self.user_dict

    # 将用户图像的features存入数据库
    def update_date(self, user_dict):
        """
        :param user_dict: 更新后的user_dict. UserID : face_features
        """
        self.is_connect()

        cursor = self.conn.cursor()

        for key, value in user_dict.items():
            userId = key
            features = value
            # sql = "UPDATE base_user SET Features= '%s' WHERE UserId = '%s'" % (features, userId)
            try:
                # 执行sql语句
                cursor.execute("UPDATE base_user SET Features= %sWHERE UserId = %s", (features, userId))
                # 提交到数据库执行
                self.conn.commit()
            except Exception as e:
                # 如果发生错误则回滚
                self.conn.rollback()
                print(e)
        cursor.close()
        self.conn.close()
        print('数据更新完成，关闭数据库连接')

    # 加载数据库中所有userID和人脸特征
    def load_features(self):
        """
        :return: 所有用户特征字典 UserID : face_features
        """
        self.is_connect()
        cursor = self.conn.cursor()
        sql = 'SELECT UserId, Features FROM Base_user'
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for item in results:
                userID = item[0]
                face_features = item[1]
                if face_features is not None:
                    self.feature_dict[userID] = face_features
        except Exception as e:
            self.conn.rollback()
            print("Error: ", e)
        return self.feature_dict

    # 获取人脸特征的方法
    def face_detect(self, img):
        """
        :param img: 经Opencv读取过的数据
        :return: 人脸特征信息
        """
        res, detected_faces = self.face_engine.ASFDetectFaces(img)
        print(detected_faces)
        if res == MOK:
            single_detected_face1 = ASF_SingleFaceInfo()
            single_detected_face1.faceRect = detected_faces.faceRect[0]
            single_detected_face1.faceOrient = detected_faces.faceOrient[0]
            res, face_feature = self.face_engine.ASFFaceFeatureExtract(img, single_detected_face1)
            if (res != MOK):
                print("ASFFaceFeatureExtract 1 fail: {}".format(res))
        else:
            print("ASFDetectFaces 1 fail: {}".format(res))

        return face_feature

    # 比较人脸特征的方法
    def similiarity(self, feature1, feature2):
        """
        :param feature1:
        :param feature2:
        :return:
        """
        res, score = self.face_engine.ASFFaceFeatureCompare(feature1, feature2)
        return res, score

    def extract_features(self, buffer_data):
        """
        :param args: 图片的二进制形式
        :return 图片的特征
        """
        #  将二进制转换成图像
        img_np_arr = np.frombuffer(buffer_data, np.uint8)
        image = cv2.imdecode(img_np_arr, cv2.IMREAD_COLOR)
        #  调用face_detect方法得出每张图片的脸部特征
        face_feature = self.face_detect(image)
        # print(face_feature)
        return face_feature
