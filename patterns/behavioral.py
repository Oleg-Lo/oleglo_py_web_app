import jsonpickle

from lo_framework.lo_templator import render


class Observer:
    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observers = []

    def notify(self):
        for item in self.observers:
            item.update(self)


class SMSNotifier(Observer):
    def update(self, subject):
        print('SMS: ', 'к нам присоединился ', subject.students[-1].name)


class EMAILNotifier(Observer):
    def update(self, subject):
        print('EMAIL: ', 'к нам присоединился ', subject.students[-1].name)


class BaseSerializer:
    def __init__(self, some_object):
        self.some_object = some_object

    def save(self):
        return jsonpickle.dumps(self.some_object)

    @staticmethod
    def load(data):
        return jsonpickle.loads(data)


# -----------------------template method---------------
class TemplateView:
    template_name = 'some_template.html'

    def get_context(self):
        return {}

    def get_template(self):
        return self.template_name

    def get_rend_templ_with_context(self):
        template_name = self.get_template()
        context = self.get_context()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.get_rend_templ_with_context()


class ListView(TemplateView):
    q_set = []
    template_name = 'list.html'
    context_obj_name = 'object_list'

    def get_queryset(self):
        # print(self.q_set)
        return self.q_set

    def get_context_obj_name(self):
        return self.context_obj_name

    def get_context(self):
        q_set = self.get_queryset()
        context_obj_name = self.get_context_obj_name()
        context = {context_obj_name: q_set}
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_req_data(req):
        return req['data']

    def create_object(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_req_data(request)
            self.create_object(data)
            return self.get_rend_templ_with_context()
        else:
            return super().__call__(request)


# -----------------------strategy---------------
class ConsoleWriter:
    def write_message(self, text):
        print(text)


class FileWriter:
    def __init__(self, file_name):
        self.file_name = file_name

    def write_message(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as file:
            file.write(text + '\n')
