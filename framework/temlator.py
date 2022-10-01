from jinja2 import FileSystemLoader
from jinja2.environment import Environment
import os


def render(template_name, folder='templates', **kwargs):
    """
    Minimum example work  with templating
    :param template_name: name teamplate
    :param folder: directory
    :param kwargs: parameters to pass to the template
    :return:
    """
    path = os.getcwd()
    full_path = os.path.join(path, folder)
    # создаем объект окружения
    env = Environment()
    # указываем папку для поиска шаблонов
    env.loader = FileSystemLoader(full_path)
    # находим шаблон в окружении
    template = env.get_template(template_name)
    return template.render(**kwargs)
