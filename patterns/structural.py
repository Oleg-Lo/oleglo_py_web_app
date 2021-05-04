from time import time


class RouteDecorator:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, page_controller_class):
        self.routes[self.url] = page_controller_class()


class DebugDecorator:
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            def timed(*args, **kwargs):
                time_start = time()
                result = method(*args, **kwargs)
                time_end = time()
                t = time_end - time_start
                print(f'метод {self.name} выполнялся {t:2.2f} ms')
                return result
            return timed
        return timeit(cls)
