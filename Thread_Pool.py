from concurrent.futures import ThreadPoolExecutor


class Thread():
    """
    线程池类
    """

    # 初始化线程池
    def __init__(self):
        # 创建一个包含10条线程的线程池
        self.pool = ThreadPoolExecutor(max_workers=10)

    def get_result(self, future):
        print(future.result())
