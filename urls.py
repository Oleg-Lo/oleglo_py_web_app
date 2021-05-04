from datetime import date
from views import Index, About, Registration, CreateCategory, CoursesList, CategoryList, CopyCourse, CreateCourse


def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

'''
routes = {'/': Index(),
          '/about/': About(),
          '/reg/': Registration(),
          '/create-category/': CreateCategory(),
          '/courses-list/': CoursesList(),
          '/create-course/': CreateCourse(),
          '/category-list/': CategoryList(),
          '/copy-course/': CopyCourse()}
'''

