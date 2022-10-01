from jsonpickle import dumps, loads
from framework.temlator import render
import os
from datetime import datetime
import time


class Observer:
    """
    интерфейс для реализации поведенчесого паттерна - "наблюдатель"
    """

    def update(self, subject):
        pass


class Subject:
    """
    класс-объект за которым будет происходить отслеживание
    """

    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SmsNotifier(Observer):
    """
    класс имитирующий отправку смс
    """

    def update(self, subject):
        print('SMS->', 'к нам присоединился', subject.students[-1].name)


class EmailNotifier(Observer):
    """
    класс имитирующий отправку эмайл
    """

    def update(self, subject):
        print(('EMAIL->', 'к нам присоединился', subject.students[-1].name))


class BaseSerializer:
    """
    класс родитель
    """

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)


class TemplateView:
    """
    класс интерфейс для реализации поведенческого паттерна - "Шаблонный метод"
    """
    template_name = 'template.html'

    def get_context_data(self, request):
        urls = request.get('urls', None),
        return {'url': urls[0]}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self, request):
        template_name = self.get_template()
        context = self.get_context_data(request)
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context(request)


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self, request):
        context = super().get_context_data(request)
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context[context_object_name] = queryset
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)
            return self.render_template_with_context(request)
        else:
            return super().__call__(request)


class ConsoleWriter:
    """
    Класс для логирования, реализация паттерна  Стратегия
    """

    def write(self, text):
        print(text)


class FileWriter:
    """
    Класс для логирования, реализация паттерна  Стратегия
    """

    def __init__(self):
        self.file_name = 'log'

    def write(self, text, name):
        if name:
            self.file_name = 'name'
        path = os.path.join(os.getcwd(), 'dir_logs')
        if not os.path.exists(path):
            os.mkdir(path)
        path_file = os.path.join(path, f'{self.file_name}.txt')
        with open(path_file, 'a', encoding='utf-8') as f:
            f.write(f'{datetime.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")} : {text}\n')
