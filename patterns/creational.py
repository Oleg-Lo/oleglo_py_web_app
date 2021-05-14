import copy
import quopri

# ---------abstract classes----------------
import sqlite3

from patterns.behavioral import ConsoleWriter, Subject
from patterns.unit_of_work import DomainObj


class User:
    def __init__(self, name):
        self.name = name


class Teacher(User):
    pass


class Student(User, DomainObj):
    def __init__(self, name):
        self.course = []
        super().__init__(name)


# -----------------------------------------


# Abstract factory pattern - фабрика пользователей
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    # Factory method pattern
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# Prototype pattern - Course
class CoursePrototype:
    def copy_course(self):
        return copy.deepcopy(self)


class Course(CoursePrototype, Subject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.course.append(self)
        self.notify()


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


# Abstract factory pattern - фабрика курсов
class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    # Factory method pattern
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# main interface
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    def find_category_by_name(self, name):
        for item in self.categories:
            print('item', item.name)
            if item.name == name:
                return item
        raise Exception(f'Нет категории с именем = {name}')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name) -> Student:
        for item in self.students:
            print(f'item={item}')
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# Singleton pattern
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']
        else:
            name = None

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):
    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        self.writer.write_message('log--->' + text)


# ------------------------------------------------------------------------------------
class StudentMapper:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()
        self.table_name = 'student'

    def get_all(self):
        sql_str = f'select * from {self.table_name}'
        self.cursor.execute(sql_str)
        res = []
        for item in self.cursor.fetchall():
            id, name = item
            student = Student(name)
            student.id = id
            res.append(student)
        return res

    def find_by_id(self):
        sql_str = f'select id,name from {self.table_name} where id=?'
        self.cursor.execute(sql_str, (id,))
        res = self.cursor.fetchone()
        if res:
            return Student(*res)
        else:
            raise DBCommitException(f'row with id={id} is not found')

    def insert(self, obj):
        sql_str = f'insert into {self.table_name} (name) values (?)'
        self.cursor.execute(sql_str, (obj.name,))
        try:
            self.conn.commit()
        except Exception as ex:
            raise DBCommitException(ex.args)

    def update(self, obj):
        sql_str = f'update {self.table_name} set name=? where id=?'
        self.cursor.execute(sql_str, (obj.name, obj.id))
        try:
            self.conn.commit()
        except Exception as ex:
            raise DBDelException(ex.args)

    def delete(self, obj):
        sql_str = f'delete from {self.table_name} where id=?'
        self.cursor.execute(sql_str, (obj.id,))
        try:
            self.conn.commit()
        except Exception as ex:
            raise DBDelException(ex.args)


class RecordNotFoundException(Exception):
    pass


class DBCommitException(Exception):
    pass


class DBUpdateException(Exception):
    pass


class DBDelException(Exception):
    pass


conn = sqlite3.connect('web_project_database.db3')


class MapperRegistry:
    mappers = {'student': StudentMapper}

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(conn)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](conn)
