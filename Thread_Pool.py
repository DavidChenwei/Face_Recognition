from concurrent.futures import ThreadPoolExecutor


class Thread():
    """
    ThreadPool Class
    """

    # Init ThreadPool
    def __init__(self):
        # Create a ThreadPool with 10 threads
        self.pool = ThreadPoolExecutor(max_workers=10)

    def get_result(self, future):
        print(future.result())

