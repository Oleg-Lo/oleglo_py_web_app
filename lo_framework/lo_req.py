import urllib


class GetReq:
    @staticmethod
    def get_req_params(environ):
        query_string = environ['QUERY_STRING']
        print(query_string)
        request_params = {}
        if query_string:
            params = query_string.split('&')
            for item in params:
                k, v = item.split('=')
                request_params[k] = urllib.parse.unquote(v)

        return request_params


class PostReq:

    @staticmethod
    def get_req_params(environ):
        data_len = environ.get('CONTENT_LENGTH')
        int_len = int(data_len) if data_len else 0
        data = environ['wsgi.input'].read(int_len) if int_len > 0 else b''

        request_params = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            params = data_str.split('&')
            for item in params:
                k, v = item.split('=')
                request_params[k] = v
        return request_params
