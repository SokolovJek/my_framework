from framework.temlator import render
from patterns.creational_patterns import Engine, Logger
from patterns.structural_pattern import UrlDecorator, Debug
from patterns.behavioural_patterns import ListView, CreateView, BaseSerializer, EmailNotifier, SmsNotifier

site = Engine()
logger = Logger('views')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()


@UrlDecorator('/')
class IndexView:
    """
    контроллер - главная страница
    """

    @Debug(name='IndexView')
    def __call__(self, request):
        return '200 OK', render('index.html',
                                object_list=request.get('data', None),
                                url=request.get('urls', None),
                                )


@UrlDecorator('/contact/')
class ContactView:

    @Debug(name='ContactView')
    def __call__(self, request):
        return '200 OK', render('contacts.html',
                                object_list=request.get('data', None),
                                url=request.get('urls'), )


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@UrlDecorator('/category/')
class CreateCategory:
    @Debug(name='CreateCategory')
    def __call__(self, request):
        if request['method'] == "POST":
            data = request['data']
            new_category = data['category']
            new_category = site.create_category(new_category)
            site.categories.append(new_category)
            logger.log('create Category')
            return '200 OK', render('index.html',
                                    object_list=request.get('data', None),
                                    url=request.get('urls', None),
                                    )
        else:
            return '200 OK', render('category_list.html',
                                    category_list=site.categories,
                                    url=request.get('urls'),
                                    )


@UrlDecorator('/create_course/')
class CreateCourse:
    @Debug(name='CreateCourse')
    def __call__(self, request):
        if request['method'] == "POST":
            data = request['data']
            name = data['name']
            price = data['price']
            category = site.find_category_by_id(self.id_category)
            new_course = site.create_course('programmer', name, category, price)

            new_course.observers.append(email_notifier)
            new_course.observers.append(sms_notifier)

            site.courses.append(new_course)
            logger.log('create course')
            return '200 OK', render('index.html',
                                    object_list=request.get('data', None),
                                    url=request.get('urls', None),
                                    )
        else:
            self.id_category = int(request['request_params']['id'])
            return '200 OK', render('create_course.html',
                                    courses=site.courses,
                                    category=site.find_category_by_id(self.id_category),
                                    url=request.get('urls'),
                                    )


@UrlDecorator('/copy_course/')
class CopyCourse:
    @Debug(name='CopyCourse')
    def __call__(self, request):
        request_params = request['request_params']
        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)
                return '200 OK', render('index.html',
                                        object_list=request.get('data', None),
                                        url=request.get('urls', None),
                                        )
        except KeyError:
            logger.log('No courses have been added yet')
            return '200 OK', 'No courses have been added yet'


@UrlDecorator('/student_list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'


@UrlDecorator('/create_student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        # name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


@UrlDecorator('/add_student/')
class AddStudentByCourseCreateView(CreateView):
    """
    Класс отвечает за добавление студентов на курс
    """
    template_name = 'add_student.html'

    def get_context_data(self, request):
        context = super().get_context_data(request)
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        # course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        # student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@UrlDecorator('/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
