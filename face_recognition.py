import traceback

import cv2
import numpy as np
import pymysql

from arcface.engine import *


class implement_method():

    def __init__(self):
        # Initialize user dictionary
        self.user_dict = {}

        # Initialize feature dictionary
        self.feature_dict = {}

        # Set APP ID and SDK KEY
        appid = b'Smxn3HaVJQN4R9TvAb5cpdd1atGLfoZHULG82XBMqhV'
        sdk_key = b'BpHQEL4momrZJK6NYKEnfxHPYsd7NN83NvzcvGQ7iLn3'

        if os.path.exists('ArcFace64.dat'):
            # 获取人脸识别引擎
            self.face_engine = ArcFace()
            print('It has been certified, and the face recognition engine is turned on')
        else:
            # Activation interface, the first need to activate online
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
            print('Passed the authentication, the face recognition engine has been turned on')

        # 需要引擎开启的功能
        self.mask = ASF_FACE_DETECT | ASF_FACERECOGNITION | ASF_AGE | ASF_GENDER | ASF_FACE3DANGLE | ASF_LIVENESS | ASF_IR_LIVENESS

        # 初始化接口
        res = self.face_engine.ASFInitEngine(ASF_DETECT_MODE_IMAGE, ASF_OP_0_ONLY, 30, 10, self.mask)
        if res != MOK:
            print("ASFInitEngine fail: {}".format(res))
        else:
            print("ASFInitEngine sucess: {}".format(res))

        #  Initialize database link
        self.conn = pymysql.connect(host='192.168.2.8', user='admin', password='admin123', database='zua_virtualcenter',
                                    charset='utf8')

    # Check if the database is connected
    def is_connect(self):
        """
        Check if the database is connected, if not, connect
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
        :return: User dictionary, <UserID : image binary data>
        """
        cursor = self.conn.cursor()
        sql = 'SELECT UserID,FaceInfo FROM base_user'
        try:
            cursor.execute(sql)
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

    # Store the features of the user image into the database
    def update_date(self, user_dict):

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
        print('The data update is complete, close the database connection')

    # Load all userID and face features in the database
    def load_features(self):
        self.is_connect()
        cursor = self.conn.cursor()
        sql = 'SELECT UserId, Features FROM Base_user'
        try:
            cursor.execute(sql)
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

    # How to get facial features
    def face_detect(self, img):
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

    # Methods for comparing facial features
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
        :param args: binary form of the picture
        :return Features of the picture
        """
        #  将二进制转换成图像
        img_np_arr = np.frombuffer(buffer_data, np.uint8)
        image = cv2.imdecode(img_np_arr, cv2.IMREAD_COLOR)
        #  调用face_detect方法得出每张图片的脸部特征
        face_feature = self.face_detect(image)
        # print(face_feature)
        return face_feature
