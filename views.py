from datetime import date

from lo_framework.lo_templator import render
from patterns.creational import Engine, Logger

site = Engine()
logger = Logger('main')


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', object_list=site.categories)
        # return '200 OK', render('index.html', data=request.get('data', None))


class About:
    def __call__(self, request):
        return '200 OK', render('about.html', data=request.get('data', None))


class Registration:
    def __call__(self, request):
        return '200 OK', render('reg.html', data=request.get('data', None))


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# контроллер - Расписания
class Schedule:
    def __call__(self, request):
        return '200 OK', render('schedule.html', data=date.today())


# контроллер - список курсов
class CoursesList:
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


# контроллер - список категорий
class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', object_list=site.categories)


# контроллер - создать категорию
class CreateCategory:
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
class CopyCourse:
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

            #return '200 OK', render('course_list.html', object_list=site.courses)
            return '200 OK', render('course_list.html',
                                    object_list=category.courses,
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# контроллер - создать курс
class CreateCourse:
    category_id = -1

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
