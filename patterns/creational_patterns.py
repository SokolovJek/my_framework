from copy import deepcopy
from quopri import decodestring
from patterns.behavioural_patterns import FileWriter, Subject


class SingletonByName(type):
    """
    порождающий паттерн Синглтон
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text, self.name)


logging = Logger('debag')


class User:
    def __init__(self, name):
        self.name = name
        logging.log(f'add new user for name {name}')


class Student(User):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class Teacher(User):
    pass


class UserFactory:
    """
    порождающий паттерн Абстрактная фабрика - фабрика пользователей
    """
    type_users = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_user, name):
        """
        порождающий паттерн Фабричный метод
        """
        try:
            return cls.type_users[type_user](name)
        except Exception:
            logging.log('Такого пользователя не существует')


class CoursePrototype:
    """
    порождающий паттерн Прототип - Курс
    """

    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype, Subject):
    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class CourseEnglish(Course):
    pass


class CourseProgrammer(Course):
    pass


class CourseFactory:
    courses = {
        'english': CourseEnglish,
        'programmer': CourseProgrammer
    }

    @classmethod
    def create(cls, curse, name, category, price):
        try:
            return cls.courses[curse](name, category, price)
        except Exception:
            logging.log('Такого курса не существует.')


# категория
class Category:
    auto_id = 0
    all_category = {
    }

    def __init__(self, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        # self.name = name
        self.category = category
        self.courses = []
        Category.all_category[self.id] = self.category

    def course_count(self):
        result = int(len(self.courses))
        # if self.category:
        #     result += self.category.course_count()
        return result


# основной интерфейс проекта
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name) -> User:
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(category) -> Category:
        return Category(category)

    def find_category_by_id(self, id) -> Category:
        for item in self.categories:
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_course(type_, name, category, price) -> Course:
        return CourseFactory.create(type_, name, category, price)

    def get_course(self, name) -> Course:
        for item in self.courses:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):

        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')

    @staticmethod
    def list_category():
        return Category.all_category

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item
