import json
import os
# import sass
import sys

# import htmlmin
# import slimit

# from dukpy import babel_compile
from glob import glob
from jinja2 import Environment, FileSystemLoader, Template
# from livereload import Server
from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer

command = sys.argv[1].replace('--', '')

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = "{}/src".format(BASE_PATH)

html_files = glob("{}/pages/**/*.html".format(SRC_PATH), recursive=True)
js_files = glob("{}/assets/js/**/*.js".format(SRC_PATH), recursive=True)
template_dir = "{}/templates".format(SRC_PATH)
data_dir = "{}/data".format(SRC_PATH)

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = ".md"

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)


@app.route('/')
def index():
    return render_template('index.html', pages=pages)


@app.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    template = page.meta.get('template', 'page.html')
    return render_template(template, page=page)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run(port=3000)


# def run_dev():
    # server = Server()
    # server.watch('./src/assets/js', 'make build_js')
    # server.watch('./src/pages', 'make build_pages')
    # server.watch('./src/templates', 'make build_pages')
    # server.watch('./src/data', 'make build_pages')
    # server.watch('./src/assets/css', 'make build_styles')
    # server.serve(root='build', port=5555)


# def build_pages():
    # pass


# def build_js():
    # for js_file in js_files:
        # with open(js_file, "r") as f:
        # with open(js_file.replace("src", "build"), "w") as b:
        # b.write(minify_js(babel_compile(f.read())['code']))


# def build_styles():
    # sass.compile(dirname=('./src/assets/css', './build/assets/css'),
        # output_style='compressed')


# def minify_js(code):
    # return slimit.minify(str(code), mangle=True, mangle_toplevel=True)


# if command == 'dev':
    # run_dev()
# elif command == 'build-pages':
    # build_pages()
# elif command == 'build-js':
    # build_js()
# elif command == 'build-styles':
    # build_styles()
# else:
     # print(f'invalid command, {command}')
