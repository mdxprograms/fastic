import os
import sass
import sys

import slimit

from dotenv import load_dotenv, find_dotenv
from dukpy import babel_compile
from glob import glob
from flask import Flask, render_template
from flask_flatpages import FlatPages
from flask_frozen import Freezer
from shutil import copyfile, rmtree

import config

load_dotenv(find_dotenv())

if os.getenv("FLASK_ENV") != "production":
    from livereload import Server

DEBUG = os.getenv("DEBUG")
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = ".md"

app = Flask(__name__)
app.config.from_object(__name__)
pages = FlatPages(app)
freezer = Freezer(app)

# slimit hack - suppress false errors
# https://github.com/rspivak/slimit/issues/97#issuecomment-464370110
slimit.lexer.ply.lex.PlyLogger = \
    slimit.parser.ply.yacc.PlyLogger = \
    type('_NullLogger', (slimit.lexer.ply.lex.NullLogger,),
         dict(__init__=lambda s, *_, **__: (None, s.super().__init__())[0]))


@app.route('/')
def index():
    pages.parent = config
    return render_template('index.html', fast=pages)


@app.route('/<path:path>/')
def page(path):
    page_data = pages.get_or_404(path)
    page_data.parent = config
    template = page_data.meta.get('template', 'page.html')
    return render_template(template, fast=page_data)


def minify_js(code):
    print("minifying js...")
    return slimit.minify(str(code), mangle=True, mangle_toplevel=True)


def build_js():
    print("building js...")

    if not os.path.exists("build/assets/js"):
        os.makedirs("build/assets/js")

    for js_file in glob("assets/js/**/*.js", recursive=True):
        with open(js_file, "r") as og:
            with open(f'./build/{js_file}', "w") as b:
                b.write(minify_js(babel_compile(og.read())['code']))


def build_styles():
    print("building styles...")

    if not os.path.exists("build/assets/css"):
        os.makedirs("build/assets/css")

    sass.compile(dirname=('./assets/sass', './build/assets/css'),
                 output_style='compressed')


def copy_images():
    print("copying images...")

    if not os.path.exists("build/assets/images"):
        os.makedirs("build/assets/images")

    for img in glob("assets/images/**/*.*", recursive=True):
        copyfile(img, f'build/{img}')


def build_pages():
    print("building site...")
    freezer.freeze()
    build_js()
    build_styles()
    copy_images()


def run_dev():
    print("starting dev...")
    server = Server()
    server.watch('./pages', build_pages)
    server.watch('./templates', build_pages)
    server.watch('./assets/sass', build_styles)
    server.watch('./assets/js', build_js)
    server.serve(root='build', port=5555)


if __name__ == '__main__':
    if os.path.exists("build"):
        rmtree("build")
        os.mkdir("build")

    if len(sys.argv) > 1 and sys.argv[1] == 'build' or os.getenv(
            "FLASK_ENV") == "production":
        build_pages()
    else:
        build_pages()
        run_dev()
