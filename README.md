# 人脸识别工程使用指南

## 运行所需库
- pymysql 1.0.2
- numpy 1.16.0
- opencv-python 4.5.3.56
- opencv-contirb-python 4.5.3.56
- flask 2.0.2

## 第一步: 获取人脸特征
用户的头像图片存储于数据库中，如果每次对比图像都需要从数据库中读取图片，然后提取图片特征，那么在并发度高的场景下，势必会造成服务器资源的浪费。  
所以要对数据库中存储的图片做一次脸部特征提取，然后存到对应的表中
运行get_face_feature.py文件即可完成此项功能。
```
python get_face_feature.py
```
或者直接进入IDE运行文件即可

## 第二步: 启动程序
运行main.py启动程序。该程序包含一个数据接口。 
```
python main.py
``` 
客户端可以请求IP:Port地址下的get_picture端口将数据传给服务器，然后服务器会返回给查询结果。  
拿到用户ID说明此人存在于数据库中，通过人脸识别  
拿到"查无此人"结果，说明人脸识别不通过。  
其中IP和Port在main.py中修改  
服务器返回的数据可以在run.py中修改。

## 其他文件解释
- Thread_Pool.py 线程池，用于处理服务器中的并发请求。
- face_recognition.py 人脸识别的封装方法。
