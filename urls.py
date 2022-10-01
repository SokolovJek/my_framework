from views import IndexView, ContactView, CreateCategory, CreateCourse, CopyCourse
from datetime import date


# block middleware
def secret_front(request):
    request['key'] = 'key'


def data_front(request):
    request['date'] = date.today()


# начал пользоваться декоратором
def data_urls(request):
    request['urls'] = {"contact": 'http://localhost:8020/contact/',
                       "index": 'http://localhost:8020/',
                       "category": 'http://localhost:8020/category/',
                       'create_course': 'http://localhost:8020/create_course/',
                       'copy_course': 'http://localhost:8020/copy_course/',
                       'student_list': 'http://localhost:8020/student_list/',
                       'create_student': 'http://localhost:8020/create_student/',
                       'add_student': 'http://localhost:8020/add_student/',
                       'api': 'http://localhost:8020/api/',
                       }


# начал пользоваться декоратором
# routes = {
#     '/': IndexView(),
#     '/contact/': ContactView(),
#     '/category/': CreateCategory(),
#     '/create_course/': CreateCourse(),
#     '/copy_course/': CopyCourse(),
# }


fronts = [
    secret_front,
    data_front,
    data_urls
]
