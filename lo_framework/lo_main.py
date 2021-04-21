# import quopri


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class FrameWork:
    def __init__(self, routes, fronts):
        self.routes_list = routes
        self.fronts_list = fronts

    def __call__(self, env, start_resp):
        path = env['PATH_INFO']
        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        method = env['REQUEST_METHOD']
        request['method'] = method
        """
        if method == 'POST':
            data = PostRequest().get_request_params(env)
            request['data'] = data
        if method == 'GET':
            data = GetRequest().get_request_params(env)
            request['request_params'] = request_params
        """
        # -------отработака паттерна page controller--------------
        if path in self.routes_list:
            view = self.routes_list[path]
        else:
            view = PageNotFound404()
        request = {}

        # --------наполнение словаря-----------
        for front in self.fronts_list:
            front(request)

        # --------start controller----------------
        code, body = view(request)
        start_resp(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]


"""
@staticmethod
def decode_val(data):
    new_data = {}
    for k, v in data.items():
        val = bytes(v.replace('%', '=').replace('+', ' '), 'utf-8')
        val_decode_str = quopri.decodestring(val).decode('utf-8')
        new_data[k] = val_decode_str
    return new_data
"""
