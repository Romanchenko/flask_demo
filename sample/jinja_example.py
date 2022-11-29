"""
Launch script from terminal
> python3 jinja_example.py

https://jinja.palletsprojects.com/en/3.0.x/templates/#builtin-tests
https://jinja.palletsprojects.com/en/2.10.x/intro/
"""

from jinja2 import Template, ModuleLoader, FileSystemLoader
from jinja2 import Environment, PackageLoader, select_autoescape


if __name__ == '__main__':
    # template = Template('Hello {{ name }}!')
    # print(template.render(name='John Doe'))

    env = Environment(
        loader=FileSystemLoader(searchpath="./templates"),
        autoescape=select_autoescape()
    )

    template = env.get_template('example2_inner.html', "exampl2.html")
    print(template.render(x=True))
    env.get_template('example2_inner.html', "exampl2.html").stream(x=True).dump('hello.html')