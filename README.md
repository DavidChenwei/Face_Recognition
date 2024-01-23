# Face Recognition User Guide

## Required libraries
- pymysql 1.0.2
- numpy 1.16.0
- opencv-python 4.5.3.56
- opencv-contirb-python 4.5.3.56
- flask 2.0.2

## First step: Get facial features
The user's avatar image is stored in the database. If each image comparison needs to read the image from the database and then extract the image features, then in the scenario of high concurrency, it will inevitably cause a waste of server resources.
Therefore, we need to extract facial features from the pictures stored in the database, and then store them in the corresponding table.

Run get_face_feature.py to implement it.
```
python get_face_feature.py
```

## Second: Start program
Run main.py to start program. The program contains a data interface. 
```
python main.py
``` 
- The client can request the get_picture port under the IP:Port address to transmit the data to the server, and then the server will return the query result.
- If program get the user ID which indicate that the person exists in the database.
- If you get the result of "No such person found", it means that the face recognition fails.
- Where IP and Port are modified in main.py
- The data returned by the server can be modified in run.py.

## Other documents explained
- Thread_Pool.py Thread pool for handling concurrent requests in the server.
- face_recognition.py API for face recognition.
-
