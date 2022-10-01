from framework.framework_request import GetRequests, PostRequest
from quopri import decodestring
from patterns.creational_patterns import Logger

logger = Logger('main')


def not_found_404_view(request):
    return '404 WHAT', '404 Page Not Found'


class Application:
    def __init__(self, routes, fronts):
        """
        :param routes: dict whis all end-points and hendlers
        :param fronts: all middleware
        """
        print('Server run .....')
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        """
        :param environ: словарь от сервера
        :param start_response: функция для ответа серверу
        """

        # получаем адрес по которому выполнен запрос
        path = environ["PATH_INFO"]

        # если нет закрывающего слеша дополняем его сами
        if not path.endswith('/'):
            path = f'{path}/'
        request = {}
        method = environ['REQUEST_METHOD']
        request['method'] = method
        if method == 'POST':
            data = PostRequest().get_request_params(environ)
            request['data'] = Application.decode_value(data)
            if request['data']:
                print(f'Нам пришёл post-запрос: {request["data"]}')
        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = Application.decode_value(request_params)
            if request['request_params']:
                print(f'Нам пришли GET-параметры:'
                      f' {request["request_params"]}')

        if path in self.routes:
            view = self.routes[path]
        else:
            view = not_found_404_view

        # передний контроллер, он добавляет все данные по запросу из промежуточного ПО
        # наполняем его, всеми данными
        # паттерн front controller
        for front in self.fronts:
            front(request)
        code, body = view(request)
        # функция которую получаем от wsgiref при вызове нашего класса
        start_response(code, [('Content-type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
