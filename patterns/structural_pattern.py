import os
import time
from datetime import datetime


class UrlDecorator:
    """
    Декоратор позволяет сохранить url обработчика
    """
    urls = {}

    def __init__(self, url):
        self.url = url
        pass

    def __call__(self, class_view):
        UrlDecorator.urls[self.url] = class_view()


# структурный паттерн - Декоратор
class Debug:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        """
        сам декоратор
        """

        # это вспомогательная функция будет декорировать каждый отдельный метод класса, см. ниже
        def timeit(method):
            """
            нужен для того, чтобы декоратор класса wrapper обернул в timeit
            каждый метод декорируемого класса
            """

            def timed(*args, **kw):
                ts = time.time()
                result = method(*args, **kw)
                te = time.time()
                delta = te - ts
                path = os.path.join(os.getcwd(), 'dir_logs')
                if not os.path.exists(path):
                    os.mkdir(path)
                path_file = os.path.join(path, f'{self.name}.txt')
                with open(path_file, 'a', encoding='utf-8') as f:
                    f.write(f'{datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")}'
                            f'{self.name} выполнялся {delta:2.2f} ms.\n')
                # print(f'debug --> {self.name} выполнялся {delta:2.2f} ms')
                return result

            return timed

        return timeit(cls)
