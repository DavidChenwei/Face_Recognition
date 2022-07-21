import json
from Thread_Pool import *
from run import run
from flask import Flask, request

app = Flask(__name__)


@app.route('/get_picture', methods=['post'])
def post_test():
    """
    :return: UserID
    """
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': 'Successfully', 'result': None}

    # 判断传入的json数据是否为空
    if len(request.get_data()) == 0:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = 'Request parameter is empty'
        return json.dumps(return_dict, ensure_ascii=False)
    try:
        # pic_binary = request.form['image']
        img = request.files.get('image')
        pic_binary = img.stream.read()
        print("二进制", pic_binary)
        future = Thread().pool.submit(run, pic_binary)
        key = future.result()
        # 对参数进行操作
        return_dict['result'] = "The current UserID is:%s" % key
    except Exception as e:
        return_dict['result'] = "errors:%s" % e
        return_dict['return_code'] = '101'
        return_dict['return_info'] = 'failed'
        print(return_dict)
    return json.dumps(return_dict, ensure_ascii=False)


if __name__ == '__main__':
    # create ThreadPool
    Thread()
    # start Data API
    app.run('192.168.2.62', threaded=True)
