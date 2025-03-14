# flask-tiny-app/flaskr/__init__.py
import os
from flask import Flask, render_template, request, redirect, url_for
import datetime

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    
    # Thêm các hàm tiện ích vào ngữ cảnh mẫu
    @app.context_processor
    def inject_utilities():
        def get_year():
            return datetime.datetime.now().year
        return {'get_year': get_year}

    @app.route('/')
    def index():
        # Chuyển hướng đến trang blog
        return redirect(url_for('blog.blog_index'))

    return app