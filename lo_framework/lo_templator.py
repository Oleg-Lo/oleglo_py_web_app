from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='pages', **kwargs):
    env = Environment()
    '''
    file_path = os.path.join(folder, template_name)
    with open(file_path, encoding='utf-8') as file:
        template = Template(file.read())
    '''
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)
