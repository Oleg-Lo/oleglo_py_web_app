import quopri
from lo_framework.lo_req import GetReq, PostReq


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

        if method == 'POST':
            post_data = PostReq().get_req_params(env)
            request['data'] = post_data
            print(f'request={request}')
            print(f'{method}: {FrameWork.decode_val(post_data)}')
        if method == 'GET':
            request_params = GetReq().get_req_params(env)
            request['request_params'] = request_params
            print(f'{method}: {request_params}')

        # -------отработака паттерна page controller--------------
        if path in self.routes_list:
            print(f'path={path}')
            view = self.routes_list[path]
        else:
            view = PageNotFound404()
        # request = {}

        # --------наполнение словаря-----------
        for front in self.fronts_list:
            front(request)

        # --------start controller----------------
        print(f'request2={request}')
        code, body = view(request)
        start_resp(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_val(data):
        new_data = {}
        for k, v in data.items():
            decode_str = quopri.decodestring(bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')).decode('UTF-8')
            new_data[k] = decode_str
            if decode_str.startswith('&#'):
                list_data_unicode = decode_str.replace('&#', '').split(";")
                data_str = ''
                for u_code in list_data_unicode:
                    if u_code:
                        data_str += chr(int(u_code))
                print(data_str)
                new_data[k] = data_str
            else:
                new_data[k] = decode_str

            """
            xx = v.replace('%', '=').replace('=26=23', '').replace('=3B', '=')
            list_data_unicode = xx.split("=")
            data_str = ''
            for u_code in list_data_unicode:
                if u_code:
                    data_str += chr(int(u_code))
            print(data_str)
            new_data[k] = data_str
            """
        return new_data


if __name__ == "__main__":
    print(quopri.decodestring('=D0=9D').decode('utf-8'))
    print(str(hex(1054)).replace('x', ''))
    # xx = '\u041e'
    print(chr(1054))
