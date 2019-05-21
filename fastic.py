import json
import os
import sass
import sys

import slimit

from dukpy import babel_compile
from glob import glob
from jinja2 import Environment, FileSystemLoader, Template
from livereload import Server
from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer


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


def minify_js(code):
    return slimit.minify(str(code), mangle=True, mangle_toplevel=True)


def build_js(dev=False):
    if not os.path.exists("build/assets/js"):
        os.mkdir("build/assets")
        os.mkdir("build/assets/js")

    for js_file in glob("assets/js/**/*.js", recursive=True):
        with open(js_file, "r") as og:
            with open(f'./build/{js_file}', "w") as b:
                if dev:
                    b.write(babel_compile(og.read())['code'])
                else:
                    b.write(minify_js(babel_compile(og.read())['code']))


def build_styles():
    sass.compile(dirname=('./assets/sass', './build/assets/css'),
                 output_style='compressed')


def run_dev():
    server = Server()
    server.watch('./templates', freezer.freeze)
    server.watch('./pages', freezer.freeze)
    server.watch('./assets/sass', build_styles)
    server.watch('./assets/js', build_js)
    server.serve(root='build', port=5555)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
        build_js()
        build_styles()
    else:
        build_js(dev=True)
        build_styles()
        run_dev()
