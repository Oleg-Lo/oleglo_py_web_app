from datetime import date

from lo_framework.lo_templator import render
from patterns.behavioral import BaseSerializer, CreateView, EMAILNotifier, SMSNotifier, ListView
from patterns.creational import Engine, Logger
from patterns.structural import RouteDecorator, DebugDecorator

site = Engine()
logger = Logger('main')
email_notifier = EMAILNotifier()
sms_notifier = SMSNotifier()

routes = {}


@RouteDecorator(routes=routes, url='/')
class Index:
    @DebugDecorator(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', object_list=site.categories)
        # return '200 OK', render('index.html', data=request.get('data', None))


@RouteDecorator(routes=routes, url='/about/')
class About:
    @DebugDecorator(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html', data=request.get('data', None))


@RouteDecorator(routes=routes, url='/reg/')
class Registration:
    @DebugDecorator(name='Registration')
    def __call__(self, request):
        return '200 OK', render('reg.html', data=request.get('data', None))


class NotFound404:
    @DebugDecorator(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# контроллер - Расписания
@RouteDecorator(routes=routes, url='/schedule/')
class Schedule:
    @DebugDecorator(name='Schedule')
    def __call__(self, request):
        return '200 OK', render('schedule.html', data=date.today())


# контроллер - список курсов
@RouteDecorator(routes=routes, url='/courses-list/')
class CoursesList:
    @DebugDecorator(name='CoursesList')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('course_list.html',
                                    object_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'Course list is empty!'


@RouteDecorator(routes=routes, url='/student-list/')
class StudentList(ListView):
    q_set = site.students
    template_name = 'student_list.html'


@RouteDecorator(routes=routes, url='/create-student/')
class CreateStudent(CreateView):
    template_name = 'create_student.html'

    def create_object(self, data):
        name = site.decode_value(data['name'])
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


# контроллер - список категорий
@RouteDecorator(routes=routes, url='/category-list/')
class CategoryList:
    @DebugDecorator(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', object_list=site.categories)


# контроллер - создать категорию
@RouteDecorator(routes=routes, url='/create-category/')
class CreateCategory:
    @DebugDecorator(name='CreateCategory')
    def __call__(self, request):
        print(request)
        if request['method'] == 'POST':
            print("request post")
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category_id = data.get('category_id')
            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)
            site.categories.append(new_category)
            return '200 OK', render('index.html', object_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


# контроллер - копировать курс
@RouteDecorator(routes=routes, url='/copy-course/')
class CopyCourse:
    @DebugDecorator(name='CopyCourse')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            category_name = request_params['category_name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'Копия_курса_{name}'
                category = site.find_category_by_name(category_name)
                print(f'category={category}')
                new_course = old_course.copy_course()

                new_course.name = new_name
                new_course.category = category
                print(f'new_course.category={new_course.category}')
                category.courses.append(new_course)
                site.courses.append(new_course)

            # return '200 OK', render('course_list.html', object_list=site.courses)
            return '200 OK', render('course_list.html',
                                    object_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# контроллер - создать курс
@RouteDecorator(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @DebugDecorator(name='CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render('course_list.html', object_list=category.courses,
                                    name=category.name, id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'Category list is empty'


@RouteDecorator(routes=routes, url='/add-student/')
class AddStudentByCourse(CreateView):
    template_name = 'add_student.html'

    def get_context(self):
        context = super().get_context()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_object(self, data):
        course_name = site.decode_value(data['course_name'])
        course = site.get_course(course_name)
        student_name = site.decode_value(data['student_name'])
        student = site.get_student(student_name)
        course.add_student(student)


@RouteDecorator(routes=routes, url='/api/')
class CourseAPI:
    @DebugDecorator(name='CourseAPI')
    def __call__(self, req):
        return '200 OK', BaseSerializer(site.courses).save()
